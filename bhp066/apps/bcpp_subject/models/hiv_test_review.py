from datetime import datetime
from django.db import models

from edc_base.audit_trail import AuditTrail
from edc.base.model.validators import date_not_future

from bhp066.apps.bcpp.choices import RECORDEDHIVRESULT_CHOICE

from .base_scheduled_visit_model import BaseScheduledVisitModel


class HivTestReview (BaseScheduledVisitModel):

    """Complete this form if HivTestingHistory.has_record."""

    hiv_test_date = models.DateField(
        verbose_name="What was the recorded date of the last HIV test?",
        validators=[date_not_future],
        help_text="Obtain this information from the card the participant presents to you.",
    )

    recorded_hiv_result = models.CharField(
        verbose_name="What was the recorded HIV test result?",
        max_length=30,
        choices=RECORDEDHIVRESULT_CHOICE,
        help_text="If the participant and written record differ, the result"
                  " from the written record should be recorded.",
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
