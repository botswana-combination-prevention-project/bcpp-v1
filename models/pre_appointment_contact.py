from django.db import models
#from django.core.exceptions import ValidationError
#from django.core.urlresolvers import reverse
from bhp_common.choices import YES_NO
from bhp_contact.models import BaseContactLogItem
from bhp_appointment.models import Appointment


class PreAppointmentContact(BaseContactLogItem):
    """Tracks contact, modifies appt_datetime, changes type and confirms and appointment."""
    appointment = models.ForeignKey(Appointment)

    is_confirmed = models.CharField(
        verbose_name='Is appointment confirmed?',
        max_length=10,
        choices=YES_NO,
        )

    def get_requires_consent(self):
        return False

    def get_subject_identifier(self):
        return self.appointment.get_subject_identifier()

    def get_report_datetime(self):
        return self.appointment.get_report_datetime()

    def post_save(self):
        """Counts number of attempts to contact and if confirmed and updated appointment."""
        dirty = False
        contact_count = self.__class__.objects.filter(appointment=self.appointment).count()
        if self.appointment.contact_count != contact_count:
            self.appointment.contact_count = contact_count
            dirty = True
        if self.__class__.objects.filter(appointment=self.appointment, is_confirmed='Yes'):
            if not self.appointment.is_confirmed:
                self.appointment.is_confirmed = True
                dirty = True
        if dirty:
            self.appointment.save()

#    def save(self, *args, **kwargs):
#        """Looks for a new_appt_datetime and decides if it can be used to modify the current appt datetime."""
#        super(PreAppointmentContact, self).save(*args, **kwargs)

    class Meta:
        app_label = 'bhp_appointment'
