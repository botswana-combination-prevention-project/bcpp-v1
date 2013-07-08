from django.db import models
from django.core.urlresolvers import reverse
from audit_trail.audit import AuditTrail
from bcpp.choices import RECORDEDHIVRESULT_CHOICE
from base_scheduled_visit_model import BaseScheduledVisitModel


class HivTestReview (BaseScheduledVisitModel):
    
    """CS002"""
    
    hiv_test_date = models.DateField(
        verbose_name="22. What was the recorded date of the last HIV test?",
        help_text="",
        )

    recorded_hiv_result = models.CharField(
        verbose_name="23. What was the recorded HIV test result?",
        max_length=30,
        choices=RECORDEDHIVRESULT_CHOICE,
        help_text="",
        )
    
    history = AuditTrail()

    def get_absolute_url(self):
        return reverse('admin:bcpp_subject_hivtestreview_change', args=(self.id,))

    class Meta:
        app_label = 'bcpp_subject'
        verbose_name = "HIV Test Review"
        verbose_name_plural = "HIV Test Review"
