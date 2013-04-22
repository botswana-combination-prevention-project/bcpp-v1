from django.db import models
from django.core.urlresolvers import reverse
from audit_trail.audit import AuditTrail
from bcpp.choices import YES_NO_DONT_ANSWER, WHYNOARV_CHOICE, ADHERENCE4DAY_CHOICE, ADHERENCE4WK_CHOICE
from base_scheduled_visit_model import BaseScheduledVisitModel


class HivCareAdherence (BaseScheduledVisitModel):
    
    """CS002"""
    
    firstpositive = models.DateTimeField(
        verbose_name = "58. When was your first positive HIV test result?",
        max_length = 25,
        help_text=("Note: If participant does not want to answer, leave blank. "
                   "If participant is unable to estimate date, record -4."),
        )

    medical_care = models.CharField(
        verbose_name = "59. Have you ever received HIV-related medical or clinical care?",
        max_length = 15,
        choices = YES_NO_DONT_ANSWER,
        help_text="",
        )

    everrecommendedarv = models.CharField(
        verbose_name = ("64. Have you ever been recommended by a doctor/nurse or other healthcare "
                        "worker to start antiretroviral therapy (ARVs), a combination of medicines "
                        "to treat your HIV infection? [common medicines include: combivir, truvada, "
                        "atripla, nevirapine]"),
        max_length = 15,
        choices = YES_NO_DONT_ANSWER,
        help_text="",
        )

    evertakearv = models.CharField(
        verbose_name = ("65. Have you ever taken any antiretroviral therapy (ARVs) for your HIV infection?"
                        " [For women: Do not include treatment that you took during pregnancy to protect "
                        "your baby from HIV]"),
        max_length = 15,
        choices = YES_NO_DONT_ANSWER,
        help_text="",
        )

    whynoarv = models.CharField(
        verbose_name = "66. What was the main reason why you have not started ARVs?",
        max_length = 15,
        choices = WHYNOARV_CHOICE,
        help_text="",
        )

    firstarv = models.DateTimeField(
        verbose_name = "67. When did you first start taking antiretroviral therapy (ARVs)?",
        max_length = 25,
        help_text=("Note: If participant does not want to answer,leave blank.  "
                   "If participant is unable to estimate date, record -4."),
        )

    onarv = models.CharField(
        verbose_name = "68. Are you currently taking antiretroviral therapy (ARVs)?",
        max_length = 15,
        choices = YES_NO_DONT_ANSWER,
        help_text="",
        )

    arv_stop = models.CharField(
        verbose_name = "69. What was the main reason why you stopped taking ARVs?",
        max_length = 15,
        choices = WHYNOARV_CHOICE,
        help_text="",
        )

    adherence4day = models.CharField(
        verbose_name = ("70. During the past 4 days, on how many days have you missed taking all your"
                        " doses of antiretroviral therapy (ART)?"),
        max_length = 15,
        choices = ADHERENCE4DAY_CHOICE,
        help_text="",
        )

    adherence4wk = models.CharField(
        verbose_name = ("71. Thinking about the past 4 weeks, on average, how would you rate your "
                        "ability to take all your medications as prescribed?"),
        max_length = 15,
        choices = ADHERENCE4WK_CHOICE,
        help_text="",
        )

    
    history = AuditTrail()

    def get_absolute_url(self):
        return reverse('admin:bcpp_subject_hivcareadherence_change', args=(self.id,))

    class Meta:
        app_label = 'bcpp_subject'
        verbose_name = "HIV care & Adherence"
        verbose_name_plural = "HIV care & Adherence"
