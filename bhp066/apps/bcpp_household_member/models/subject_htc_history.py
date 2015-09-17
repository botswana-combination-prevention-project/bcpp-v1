from datetime import datetime

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django_extensions.db.fields import UUIDField

from edc.choices import YES_NO

from edc.base.model.models import BaseUuidModel

from bhp066.apps.bcpp_survey.models import Survey

from .household_member import HouseholdMember


class SubjectHtcHistory(BaseUuidModel):
    """A system model that tracks the history of deleted subject HTC instances."""
    transaction = UUIDField()

    household_member = models.ForeignKey(HouseholdMember)

    report_datetime = models.DateTimeField(
        verbose_name="Report date",
        default=datetime.today())

    survey = models.ForeignKey(Survey, editable=False)

    tracking_identifier = models.CharField(
        verbose_name=_("HTC tracking identifier"),
        max_length=50,
        null=True,
        blank=True,
        help_text='Transcribe this tracking identifier onto the paper HTC Intake form.')

    offered = models.CharField(
        verbose_name=_("Was the subject offered HTC"),
        max_length=10,
        choices=YES_NO)

    accepted = models.CharField(
        verbose_name=_("Did the subject accept HTC"),
        max_length=25,
        choices=YES_NO)

    refusal_reason = models.CharField(
        verbose_name=_("If the subject did not accept HTC, please explain"),
        max_length=50,
        null=True,
        blank=True,
        help_text='Required if subject did not accepted HTC')

    referred = models.CharField(
        verbose_name=_("Was the subject referred"),
        max_length=10,
        choices=YES_NO,
        help_text='Required if subject accepted HTC')

    referral_clinic = models.CharField(
        verbose_name=_("If referred, which clinic"),
        max_length=25,
        blank=True,
        null=True,
        help_text='Required if subject was referred')

    comment = models.TextField(max_length=250, null=True, blank=True)

    def natural_key(self):
        return (self.transaction, )

    def get_report_datetime(self):
        return self.report_datetime

    def get_registration_datetime(self):
        return self.report_datetime

    class Meta:
        app_label = 'bcpp_household_member'
        verbose_name = 'Subject Htc History'
