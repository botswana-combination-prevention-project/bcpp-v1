from django.db import models
from django.core.urlresolvers import reverse
from audit_trail.audit import AuditTrail
from bcpp.choices import EDUCATION_CHOICE, EMPLOYMENT_CHOICE, YES_NO_DONT_ANSWER
from bcpp_subject.choices import MONTHLY_INCOME
from base_scheduled_visit_model import BaseScheduledVisitModel


class Education (BaseScheduledVisitModel):
    
    """CS002"""
    
    education = models.CharField(
        verbose_name = "12. What is your highest level of education attainment?",
        max_length = 15,
        choices = EDUCATION_CHOICE,
        help_text="",
        )

    employment = models.CharField(
        verbose_name = "13. What is your current employment [working for payment] status?",
        max_length = 15,
        choices = EMPLOYMENT_CHOICE,
        help_text="",
        )

    moneyforwork  = models.CharField(
        verbose_name = "14. In the past month, how much money did you earn from work you did?",
        max_length = 15,
        choices = MONTHLY_INCOME,
        help_text="",
        )

    seekingwork = models.CharField(
        verbose_name = "15. Are you currently seeking [more] employment?",
        max_length = 15,
        choices = YES_NO_DONT_ANSWER,
        help_text="",
        )
    
    history = AuditTrail()

    def get_absolute_url(self):
        return reverse('admin:bcpp_subject_education_change', args=(self.id,))

    class Meta:
        app_label = 'bcpp_subject'
        verbose_name = "Education"
        verbose_name_plural = "Education"
