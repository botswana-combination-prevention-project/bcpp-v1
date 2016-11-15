from django.db import models

from django_crypto_fields.fields import EncryptedCharField, EncryptedTextField

from edc_base.model.models import BaseUuidModel
from edc_base.model.validators import datetime_not_future, date_not_future
from edc_base.model.fields import OtherCharField

from bcpp_survey.models import Survey

from ..choices import NEXT_APPOINTMENT_SOURCE

from .household_member import HouseholdMember


class HouseholdMemberModelMixin(BaseUuidModel):

    """ Base for membership form models that need a foreignkey to
    the registered subject and household_member model"""

    household_member = models.OneToOneField(HouseholdMember)

    report_datetime = models.DateTimeField(
        verbose_name="Report date",
        validators=[
            datetime_not_future, ],
        auto_now=False)

    survey = models.ForeignKey(Survey, editable=False)

    def __str__(self):
        return str(self.household_member)

    def natural_key(self):
        return self.household_member.natural_key()
    natural_key.dependencies = ['bcpp_household_member.householdmember', ]

    def confirm_registered_subject_pk_on_post_save(self, using):
        if self.registered_subject.pk != self.household_member.registered_subject.pk:
            raise TypeError('Expected self.registered_subject.pk == self.household_member.'
                            'registered_subject.pk. Got {0} != {1}.'.format(
                                self.registered_subject.pk, self.household_member.registered_subject.pk))

    class Meta:
        abstract = True
        ordering = ['household_member']


class SubjectEntryMixin(models.Model):
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
