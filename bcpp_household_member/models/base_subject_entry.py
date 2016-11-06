from django.db import models
from django_crypto_fields.fields import EncryptedCharField, EncryptedTextField

from edc_base.model.fields import OtherCharField
from edc_base.model.models import BaseUuidModel
from edc_base.model.validators import date_not_future
from edc_sync.model_mixins import SyncModelMixin

from ..choices import NEXT_APPOINTMENT_SOURCE


class BaseSubjectEntry(SyncModelMixin, BaseUuidModel):
    """For absentee and undecided log models."""
    report_datetime = models.DateField(
        verbose_name="Report date",
        validators=[date_not_future])

    reason_other = OtherCharField()

    next_appt_datetime = models.DateTimeField(
        verbose_name="Follow-up appointment",
        help_text="The date and time to meet with the subject")

    next_appt_datetime_source = models.CharField(
        verbose_name="Appointment date suggested by?",
        max_length=25,
        choices=NEXT_APPOINTMENT_SOURCE,
        help_text='')

    contact_details = EncryptedCharField(
        null=True,
        blank=True,
        help_text='Information that can be used to contact someone, '
                  'preferrably the subject, to confirm the appointment')

    comment = EncryptedTextField(
        verbose_name="Comments",
        max_length=250,
        blank=True,
        null=True,
        help_text=('IMPORTANT: Do not include any names or other personally identifying '
                   'information in this comment'))

    class Meta:
        abstract = True
