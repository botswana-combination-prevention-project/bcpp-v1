from datetime import datetime
from django.db import models
from django.utils.translation import ugettext as _
from audit_trail.audit import AuditTrail
from bcpp.choices import RECORDEDHIVRESULT_CHOICE
from base_scheduled_visit_model import BaseScheduledVisitModel


class HivTestReview (BaseScheduledVisitModel):

    hiv_test_date = models.DateField(
        verbose_name=_("What was the recorded date of the last HIV test?"),
        help_text="Obtain this information from the card the participant presents to you.",
        )

    recorded_hiv_result = models.CharField(
        verbose_name=_("What was the recorded HIV test result?"),
        max_length=30,
        choices=RECORDEDHIVRESULT_CHOICE,
        help_text=("If the participant and written record differ, the result"
                   " from the written record should be recorded."),
        )

    history = AuditTrail()

    def get_test_code(self):
        return 'HIV'

    def get_result_datetime(self):
        return datetime(self.hiv_test_date.year, self.hiv_test_date.month, self.hiv_test_date.day)

    class Meta:
        app_label = 'bcpp_subject'
        verbose_name = "HIV Test Review"
        verbose_name_plural = "HIV Test Review"
