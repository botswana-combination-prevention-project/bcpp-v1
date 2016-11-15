from django.db import models
from django.utils import timezone

from edc_base.model.fields import OtherCharField
from edc_base.model.models import BaseUuidModel, HistoricalRecords

from bcpp.manager_mixins import CurrentCommunityManagerMixin
from bcpp_survey.models import Survey

from ..choices import WHY_NOPARTICIPATE_CHOICE
from ..managers import SubjectRefusalHistoryManager

from .household_member import HouseholdMember


class SubjectRefusalHistoryManager(CurrentCommunityManagerMixin, models.Manager):

    lookup = ['household_member', 'household_structure', 'household', 'plot']

    def get_by_natural_key(self, transaction):
        return self.get(transaction=transaction)


class SubjectRefusalHistory(BaseUuidModel):
    """A system model that tracks the history of deleted refusal instances."""

    transaction = models.UUIDField()

    household_member = models.ForeignKey(HouseholdMember)

    report_datetime = models.DateTimeField(
        verbose_name="Report date",
        default=timezone.now)

    survey = models.ForeignKey(Survey, editable=False)

    refusal_date = models.DateField(
        verbose_name="Date subject refused participation",
        help_text="Date format is YYYY-MM-DD")

    reason = models.CharField(
        verbose_name=("We respect your decision to decline. It would help us"
                      " improve the study if you could tell us the main reason"
                      " you do not want to participate in this study?"),
        max_length=50,
        choices=WHY_NOPARTICIPATE_CHOICE,
        help_text="",
    )
    reason_other = OtherCharField()

    objects = SubjectRefusalHistoryManager()

    history = HistoricalRecords()

    def natural_key(self):
        return (self.transaction, )

    def get_report_datetime(self):
        return self.report_datetime

    def get_registration_datetime(self):
        return self.report_datetime

    class Meta:
        app_label = 'bcpp_household_member'
        verbose_name = 'Subject Refusal History'
