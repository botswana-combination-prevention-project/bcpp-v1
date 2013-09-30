from datetime import datetime
from django.db import models
from django.utils.translation import ugettext as _
from edc.audit.audit_trail import AuditTrail
from bcpp.choices import HIV_RESULT, WHYNOHIVTESTING_CHOICE
from .base_scheduled_visit_model import BaseScheduledVisitModel


class HivResult (BaseScheduledVisitModel):

    hiv_result = models.CharField(
        verbose_name=_("Today\'s HIV test result"),
        max_length=50,
        choices=HIV_RESULT,
        help_text="If participant declined HIV testing, please select a reason below.",
        )

    hiv_result_datetime = models.DateTimeField(
        verbose_name=_("Today\'s HIV test result date and time"),
        )

    why_not_tested = models.CharField(
        verbose_name=_("What was the main reason why you did not want HIV testing"
                       " as part of today's visit?"),
        max_length=65,
        null=True,
        blank=True,
        choices=WHYNOHIVTESTING_CHOICE,
        help_text="Note: Only asked of individuals declining HIV testing during this visit.",
        )

    history = AuditTrail()

    def get_test_code(self):
        return 'HIV'

    def get_result_datetime(self):
        return datetime(self.hiv_result_datetime.year, self.hiv_result_datetime.month, self.hiv_result_datetime.day)

    class Meta:
        app_label = "bcpp_subject"
        verbose_name = "Today\'s HIV Result"
        verbose_name_plural = "Today\'s HIV Result"
