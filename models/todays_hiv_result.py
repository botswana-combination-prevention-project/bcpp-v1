from django.db import models
from audit_trail.audit import AuditTrail
from django.core.urlresolvers import reverse
from bcpp.choices import HHHIVTEST_CHOICE
from base_scheduled_visit_model import BaseScheduledVisitModel


class TodaysHivResult (BaseScheduledVisitModel):
    
    hiv_result = models.CharField(
        verbose_name="Record today\'s HIV test result:",
        max_length=50,
        choices=HHHIVTEST_CHOICE,
        help_text="",
        )
    
    history = AuditTrail()
     
    def get_absolute_url(self):
        return reverse('admin:bcpp_subject_todayshivresult_change', args=(self.id,))

    """CS002"""
    
    class Meta:
        app_label = "bcpp_subject"
        verbose_name ="Today\'s HIV Result"
        verbose_name_plural ="Today\'s HIV Result"
