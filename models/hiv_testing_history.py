from django.db import models
from django.core.urlresolvers import reverse
from audit_trail.audit import AuditTrail
from bcpp.choices import YES_NO_UNSURE, WHYNOHIVTESTING_CHOICE, YES_NO_DONT_ANSWER, WHENHIVTEST_CHOICE, VERBALHIVRESULT_CHOICE
from bcpp_subject.choices import YES_NO_RECORD_REFUSAL
from base_scheduled_visit_model import BaseScheduledVisitModel


class HivTestingHistory (BaseScheduledVisitModel):

    """CS002"""

    take_hiv_testing = models.CharField(
        verbose_name="16. Would you like to take an HIV testing today?",
        max_length=75,
        choices=YES_NO_UNSURE,
        help_text="",
        )

    why_not_tested = models.CharField(
        verbose_name="17. What was the main reason why you did not want HIV testing as part of today's visit?",
        max_length=65,
        null=True,
        blank=True,
        choices=WHYNOHIVTESTING_CHOICE,
        help_text="Note: Only asked of individuals declining HIV testing during this visit.",
        )

    has_tested = models.CharField(
        verbose_name="18. Have you ever been tested for HIV before?",
        max_length=15,
        choices=YES_NO_DONT_ANSWER,
        help_text="",
        )

    has_record = models.CharField(
        verbose_name="19. Is a record of last HIV test [OPD card, Tebelopele, other] available to review?",
        max_length=45,
        null=True,
        blank=True,
        choices=YES_NO_RECORD_REFUSAL,
        help_text="",
        )
    
    when_hiv_test = models.CharField(
        verbose_name=("20. When was the last [most recent]"
                        " time you were tested for HIV?"),
        max_length=25,
        null=True,
        blank=True,
        choices=WHENHIVTEST_CHOICE,
        help_text="",
        )

    verbal_hiv_result = models.CharField(
        verbose_name="21. Please tell me the results of your last [most recent] HIV test?",
        max_length=30,
        null=True,
        blank=True,
        choices=VERBALHIVRESULT_CHOICE,
        help_text="",
        )


    history = AuditTrail()

    def get_absolute_url(self):
        return reverse('admin:bcpp_subject_hivtestinghistory_change', args=(self.id,))

    class Meta:
        app_label = 'bcpp_subject'
        verbose_name = "Hiv Testing History"
        verbose_name_plural = "Hiv Testing History"
