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

    new_appt_datetime = models.DateTimeField(
        verbose_name='Change appointment date/time to:',
        null=True,
        blank=True,
        help_text='Complete only if subject wishes to change appointment date')

    def get_requires_consent(self):
        return False

    def get_subject_identifier(self):
        return self.appointment.get_subject_identifier()

    def get_report_datetime(self):
        return self.appointment.get_report_datetime()

#    def modify_appt_datetime(self, exception_cls=None):
#        if not exception_cls:
#            exception_cls = ValidationError

    def save(self, *args, **kwargs):
        """Looks for a new_appt_datetime and decides if it can be used to modify the current appt datetime."""
        if self.new_appt_datetime:
            self.appointment.appt_datetime = self.new_appt_datetime
            self.appointment.save()
        super(PreAppointmentContact, self).save(*args, **kwargs)

    class Meta:
        app_label = 'bhp_appointment'
