from django.db import models
#from django.core.exceptions import ValidationError
#from django.core.urlresolvers import reverse
from audit_trail.audit import AuditTrail
from bhp_contact.models import BaseContactLogItem
from bhp_appointment.models import Appointment


class PreAppointmentContact(BaseContactLogItem):
    """Tracks contact, modifies appt_datetime, changes type and confirms and appointment."""
    appointment = models.ForeignKey(Appointment)

    is_confirmed = models.BooleanField(
        verbose_name='Appointment confirmed',
        default=False,
        )

    history = AuditTrail()

    objects = models.Manager()

    def get_requires_consent(self):
        return False

    def get_subject_identifier(self):
        return self.appointment.get_subject_identifier()

    def get_report_datetime(self):
        return self.appointment.get_report_datetime()

    def recalc_contact_count(self, dirty):
        contact_count = self.__class__.objects.filter(appointment=self.appointment).count()
        if self.appointment.contact_count != contact_count:
            self.appointment.contact_count = contact_count
            dirty = True
        return dirty, contact_count

    def recalc_is_confirmed(self, dirty, **kwargs):
        is_confirmed = kwargs.get('is_confirmed', self.is_confirmed)
        if is_confirmed:
            # if not already confirmed in a previous or following instance, update
            if not self.__class__.objects.filter(appointment=self.appointment, is_confirmed=True).exclude(pk=self.pk):
                self.appointment.is_confirmed = True
                dirty = True
        elif not self.__class__.objects.filter(appointment=self.appointment, is_confirmed=True) and self.appointment.is_confirmed:
            self.appointment.is_confirmed = False
            dirty = True
        return dirty

    def post_save(self):
        """Counts number of attempts to contact and if confirmed and updated appointment.

        Once confirmed, the appointment instance remains flagged as confirmed."""
        dirty = False
        dirty, contact_count = self.recalc_contact_count(dirty)
        dirty = self.recalc_is_confirmed(dirty)
        if dirty:
            self.appointment.save()
        return contact_count, self.is_confirmed, dirty

    def post_delete(self):
        dirty = False
        dirty, contact_count = self.recalc_contact_count(dirty)
        dirty = self.recalc_is_confirmed(dirty, is_confirmed=False)
        if dirty:
            self.appointment.save()
        return contact_count, self.is_confirmed, dirty

    def __unicode__(self):
        return unicode(self.appointment)

#    def save(self, *args, **kwargs):
#        """Looks for a new_appt_datetime and decides if it can be used to modify the current appt datetime."""
#        super(PreAppointmentContact, self).save(*args, **kwargs)

    class Meta:
        app_label = 'bhp_appointment'
