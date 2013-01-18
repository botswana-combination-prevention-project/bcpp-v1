from django.db import models
from django.utils.translation import ugettext_lazy as _
from bhp_appointment.choices import APPT_STATUS
from bhp_consent.models import BaseConsentedUuidModel


class BaseAppointment (BaseConsentedUuidModel):
    """Base class for Appointments."""
    appt_datetime = models.DateTimeField(
        verbose_name=_("Appointment date and time"),
        help_text="",
        db_index=True)
    # this is the original calculated appointment datetime
    # which the user cannot change
    timepoint_datetime = models.DateTimeField(
        verbose_name=_("Timepoint date and time"),
        help_text="calculated appointment datetime. Do not change",
        null=True,
        editable=False)
    appt_status = models.CharField(
        verbose_name=_("Status"),
        choices=APPT_STATUS,
        max_length=25,
        default='new',
        db_index=True)
    appt_reason = models.CharField(
        verbose_name=_("Reason for appointment"),
        max_length=25,
        help_text=_("Reason for appointment"),
        blank=True)
    contact_tel = models.CharField(
        verbose_name=_("Contact Tel"),
        max_length=250,
        blank=True)
    comment = models.CharField("Comment",
        max_length=250,
        blank=True)

    def get_report_datetime(self):
        return self.appt_datetime
    
    class Meta:
        abstract = True
