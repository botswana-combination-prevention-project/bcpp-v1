from datetime import datetime

from django.db import models

from edc.base.model.fields import OtherCharField, UUIDField

from edc.device.dispatch.models import BaseDispatchSyncUuidModel

from apps.bcpp.choices import WHYNOPARTICIPATE_CHOICE
from apps.bcpp_household.models import Plot
from apps.bcpp_survey.models import Survey

from ..managers import SubjectRefusalHistoryManager

from .household_member import HouseholdMember


class SubjectRefusalHistory(BaseDispatchSyncUuidModel):

    transaction = UUIDField()

    household_member = models.ForeignKey(HouseholdMember)

    report_datetime = models.DateTimeField("Report date",
        default=datetime.today())

    survey = models.ForeignKey(Survey, editable=False)

    refusal_date = models.DateField(
        verbose_name="Date subject refused participation",
        help_text="Date format is YYYY-MM-DD")

    reason = models.CharField(
        verbose_name=("We respect your decision to decline. It would help us"
                      " improve the study if you could tell us the main reason"
                      " you do not want to participate in this study?"),
        max_length=50,
        choices=WHYNOPARTICIPATE_CHOICE,
        help_text="",
        )
    reason_other = OtherCharField()

    objects = SubjectRefusalHistoryManager()

    def natural_key(self):
        return (self.transaction, )

    def dispatch_container_lookup(self, using=None):
        return (Plot, 'household_member__household_structure__household__plot__plot_identifier')

    def is_dispatchable(self):
        return True

    def get_report_datetime(self):
        return self.report_datetime

    def get_registration_datetime(self):
        return self.report_datetime

    def dispatch_item_container_reference(self, using=None):
        return (('bcpp_household', 'plot'), 'household_member__household_structure__household__plot')

    class Meta:
        app_label = 'bcpp_household_member'
        verbose_name = 'Subject Refusal History'
