from django.db import models
from audit_trail.audit import AuditTrail
from bcpp.choices import EDUCATION_CHOICE, EMPLOYMENT_CHOICE, YES_NO_DONT_ANSWER
from bcpp_subject.choices import MONTHLY_INCOME
from base_scheduled_visit_model import BaseScheduledVisitModel


class Education (BaseScheduledVisitModel):

    """CS002"""

    education = models.CharField(
        verbose_name="12. What is your highest level of education attainment?",
        max_length=65,
        choices=EDUCATION_CHOICE,
        help_text="",
        )

    employment = models.CharField(
        verbose_name="13. What is your current employment [working for payment] status?",
        max_length=35,
        choices=EMPLOYMENT_CHOICE,
        help_text="",
        )

    money_forwork = models.CharField(
        verbose_name="14. In the past month, how much money did you earn from work you did?",
        max_length=25,
        null=True, 
        blank=True,
        choices=MONTHLY_INCOME,
        help_text="",
        )

    seeking_work = models.CharField(
        verbose_name="15. Are you currently seeking [more] employment?",
        max_length=25,
        choices=YES_NO_DONT_ANSWER,
        help_text="",
        )

    history = AuditTrail()

    class Meta:
        app_label = 'bcpp_subject'
        verbose_name = "Education"
        verbose_name_plural = "Education"
