from django.db import models
from django.core.urlresolvers import reverse
from audit_trail.audit import AuditTrail
from bcpp.choices import RECORDEDHIVRESULT_CHOICE, WHENHIVTEST_CHOICE, VERBALHIVRESULT_CHOICE
from base_scheduled_visit_model import BaseScheduledVisitModel


class HivTestReview (BaseScheduledVisitModel):
    
    """CS002"""
    
    hivtestdate = models.DateTimeField(
        verbose_name = "20. What was the recorded date of the last HIV test?",
        max_length = 25,
        null=True, 
        blank=True,
        help_text=("Note:If participant does not want to answer, leave blank.  "
                   "If participant is unable to estimate date, record estimation."),
        )

    recordedhivresult = models.CharField(
        verbose_name = "21. What was the recorded HIV test result?",
        max_length = 15,
        choices = RECORDEDHIVRESULT_CHOICE,
        help_text="",
        )

    whenhivtest = models.CharField(
        verbose_name = ("22. Not including today's HIV test, when was the last [most recent]"
                        " time you were tested for HIV?"),
        max_length = 15,
        choices = WHENHIVTEST_CHOICE,
        help_text="",
        )

    verbalhivresult = models.CharField(
        verbose_name = "23. Please tell me the results of your last [most recent] HIV test?",
        max_length = 15,
        choices = VERBALHIVRESULT_CHOICE,
        help_text="",
        )
    
    history = AuditTrail()

    def get_absolute_url(self):
        return reverse('admin:bcpp_subject_hivtestreview_change', args=(self.id,))

    class Meta:
        app_label = 'bcpp_subject'
        verbose_name = "HIV Test Review"
        verbose_name_plural = "HIV Test Review"
