from django.db import models
from django.core.urlresolvers import reverse
from audit_trail.audit import AuditTrail
from bcpp.choices import RECORDEDHIVRESULT_CHOICE, WHENHIVTEST_CHOICE, VERBALHIVRESULT_CHOICE
from base_scheduled_visit_model import BaseScheduledVisitModel


class HivTestReview (BaseScheduledVisitModel):
    
    """CS002 - [numbering here has been re-arranged. Not same as in Wiki. sl note. ]"""
    
    hiv_test_date = models.DateField(
        verbose_name="22. What was the recorded date of the last HIV test?",
        null=True,
        blank=True,
        help_text=("Note:If participant does not want to answer, leave blank.  "
                   "If participant is unable to estimate date, record estimation."),
        )

    recorded_hiv_result = models.CharField(
        verbose_name="23. What was the recorded HIV test result?",
        max_length=30,
        null=True,
        blank=True,
        choices=RECORDEDHIVRESULT_CHOICE,
        help_text="",
        )

    when_hiv_test = models.CharField(
        verbose_name=("20. When was the last [most recent]"
                        " time you were tested for HIV?"),
        max_length=25,
        choices=WHENHIVTEST_CHOICE,
        help_text="",
        )

    verbal_hiv_result = models.CharField(
        verbose_name="21. Please tell me the results of your last [most recent] HIV test?",
        max_length=30,
        choices=VERBALHIVRESULT_CHOICE,
        help_text="",
        )
    
    history = AuditTrail()

    def get_absolute_url(self):
        return reverse('admin:bcpp_subject_hivtestreview_change', args=(self.id,))

    class Meta:
        app_label = 'bcpp_subject'
        verbose_name = "HIV Test Review"
        verbose_name_plural = "HIV Test Review"
