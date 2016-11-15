from django.db import models
from django.utils import timezone
from django_extensions.db.fields import UUIDField

from edc_base.model.models import BaseUuidModel, HistoricalRecords
from edc_constants.choices import YES_NO

from bcpp_survey.models import Survey

from .household_member import HouseholdMember


class SubjectHtcHistoryManager(models.Manager):

    lookup = ['subject_refusal', 'household_member', 'household_structure', 'household', 'plot']

    def get_by_natural_key(self, transaction):
        self.get(transaction=transaction)


class SubjectHtcHistory(BaseUuidModel):
    """A system model that tracks the history of deleted subject HTC instances."""
    transaction = UUIDField(unique=True)

    household_member = models.ForeignKey(HouseholdMember)

    report_datetime = models.DateTimeField(
        verbose_name="Report date",
        default=timezone.now)

    survey = models.ForeignKey(Survey, editable=False)

    tracking_identifier = models.CharField(
        verbose_name="HTC tracking identifier",
        max_length=50,
        null=True,
        blank=True,
        help_text='Transcribe this tracking identifier onto the paper HTC Intake form.')

    offered = models.CharField(
        verbose_name="Was the subject offered HTC",
        max_length=10,
        choices=YES_NO)

    accepted = models.CharField(
        verbose_name="Did the subject accept HTC",
        max_length=25,
        choices=YES_NO)

    refusal_reason = models.CharField(
        verbose_name="If the subject did not accept HTC, please explain",
        max_length=50,
        null=True,
        blank=True,
        help_text='Required if subject did not accepted HTC')

    referred = models.CharField(
        verbose_name="Was the subject referred",
        max_length=10,
        choices=YES_NO,
        help_text='Required if subject accepted HTC')

    referral_clinic = models.CharField(
        verbose_name="If referred, which clinic",
        max_length=25,
        blank=True,
        null=True,
        help_text='Required if subject was referred')

    comment = models.TextField(max_length=250, null=True, blank=True)

    objects = SubjectHtcHistoryManager()

    history = HistoricalRecords()

    def natural_key(self):
        return (self.transaction, )

    def get_report_datetime(self):
        return self.report_datetime

    def get_registration_datetime(self):
        return self.report_datetime

    class Meta:
        app_label = 'bcpp_household_member'
        verbose_name = 'Subject Htc History'
