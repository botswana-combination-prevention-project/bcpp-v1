from django.db import models
from django.core.urlresolvers import reverse
from audit_trail.audit import AuditTrail
from bcpp.choices import WHEREHIVTEST_CHOICE, WHYHIVTEST_CHOICE, WHYNOHIVTEST_CHOICE, YES_NO_UNSURE
from base_scheduled_visit_model import BaseScheduledVisitModel


class HivTestingSupplemental (BaseScheduledVisitModel):
    
    """CS002"""
    
    numhivtests = models.IntegerField(
        verbose_name = "Supplemental HT1. How many times before today have you had an HIV test?",
        max_length = 2,
        help_text="Note:Leave blank if participant does not want to respond.",
        )

    wherehivtest = models.CharField(
        verbose_name = "Supplemental HT2. Not including today's HIV test, where were you tested for HIV, the last [most recent] time you were tested?",
        max_length = 15,
        choices = WHEREHIVTEST_CHOICE,
        help_text="",
        )

    whyhivtest = models.CharField(
        verbose_name = "Supplemental HT3. Not including today's HIV test, which of the following statements best describes the reason you were tested the last [most recent] time you were tested before today?",
        max_length = 15,
        choices = WHYHIVTEST_CHOICE,
        help_text="",
        )

    whynohivtest = models.CharField(
        verbose_name = "Supplemental HT4. If you were not tested for HIV in the 12 months prior to today, what is the main reason why not?",
        max_length = 15,
        choices = WHYNOHIVTEST_CHOICE,
        help_text="",
        )

    hiv_pills = models.CharField(
        verbose_name = "Supplemental HT5. Have you ever heard about treatment for HIV with pills called antiretroviral therapy or ARVs [or HAART]?",
        max_length = 15,
        choices = YES_NO_UNSURE,
        help_text="",
        )

    arvshivtest = models.CharField(
        verbose_name = "Supplemental HT6. Do you believe that treatment for HIV with antiretroviral therapy (or ARVs) can help HIV-positive people to live longer?",
        max_length = 15,
        choices = YES_NO_UNSURE,
        help_text="",
        )

    prefer_hivtest = models.CharField(
        verbose_name = "Supplemental HT7. In the future, where would you prefer to get tested for HIV?",
        max_length = 15,
        choices = WHYNOHIVTEST_CHOICE,
        help_text="",
        )

    hivtest_time = models.CharField(
        verbose_name = "Supplemental HT8. In the future, is there a particular time of day that you would prefer to receive your next HIV test ?",
        max_length = 15,
        choices = WHYNOHIVTEST_CHOICE,
        help_text="",
        )

    hivtest_week = models.CharField(
        verbose_name = "Supplemental HT9. In the future, is there a particular day of the week that you would prefer to receive your next HIV test ?",
        max_length = 15,
        choices = WHYNOHIVTEST_CHOICE,
        help_text="",
        )

    hivtest_year = models.CharField(
        verbose_name = "Supplemental HT10. In the future, is there a particular time of year that you would prefer to receive your next HIV test?",
        max_length = 15,
        choices = WHYNOHIVTEST_CHOICE,
        help_text="",
        )
    
    history = AuditTrail()

    def get_absolute_url(self):
        return reverse('admin:bcpp_subject_supplementalht_change', args=(self.id,))

    class Meta:
        app_label = 'bcpp_subject'
        verbose_name = "Supplemental HT"
        verbose_name_plural = "Supplemental HT"
