from django.db import models
from django.core.urlresolvers import reverse
from audit_trail.audit import AuditTrail
from bcpp.choices import HHHIVTEST_CHOICE, WHYNOHIVTEST_CHOICE, YES_NO_DONT_ANSWER
from base_scheduled_visit_model import BaseScheduledVisitModel


class HivTestingHistory (BaseScheduledVisitModel):
    
    """CS002"""
    
    HHhivtest = models.CharField(
        verbose_name = "16. [For Interviewer:] What was the result of today's HIV test result?",
        max_length = 15,
        choices = HHHIVTEST_CHOICE,
        help_text="",
        )

    whynohivtest = models.CharField(
        verbose_name = "17. What was the main reason why you did not want HIV testing as part of today's visit?",
        max_length = 15,
        choices = WHYNOHIVTEST_CHOICE,
        help_text="Note: Only asked of individuals declining HIV testing during this visit.",
        )

    everhivtest = models.CharField(
        verbose_name = "18. Not including today's HIV test, have you ever been tested for HIV before?",
        max_length = 15,
        choices = YES_NO_DONT_ANSWER,
        help_text="",
        )
    
    hivtestrecord = models.CharField(
        verbose_name = "19. Is a record of last HIV test [OPD card, Tebelopele, other] available to review?",
        max_length = 15,
        choices = YES_NO_DONT_ANSWER,
        help_text="",
        )
    
    history = AuditTrail()

    def get_absolute_url(self):
        return reverse('admin:bcpp_subject_hivtestinghistory_change', args=(self.id,))

    class Meta:
        app_label = 'bcpp_subject'
        verbose_name = "Hiv Testing History"
        verbose_name_plural = "Hiv Testing History"
