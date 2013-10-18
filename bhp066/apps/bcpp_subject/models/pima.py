from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator

from edc.audit.audit_trail import AuditTrail
from edc.choices.common import YES_NO

from .base_scheduled_visit_model import BaseScheduledVisitModel


class Pima (BaseScheduledVisitModel):

    """CS002 - Used for PIMA cd4 count recording"""

    pima_today = models.CharField(
        verbose_name=("Was a PIMA CD4 done today?"),
        choices=YES_NO,
        max_length=3,
        help_text="",
        )

    pima_today_other = models.CharField(
        verbose_name=("If no PIMA CD4 today, please explain why"),
        max_length=50,
        null=True,
        blank=True,
        )

    pima_id = models.CharField(
        verbose_name="What is the PIMA CD4 ID?",
        max_length=9,
        validators=[RegexValidator(regex='\d+', message='PIMA ID must be a two digit number.')],
        null=True,
        blank=True,
        help_text="type this id directly from the machine as labeled")

    cd4_value = models.DecimalField(
        verbose_name=("What is the CD4 count of the PIMA machine?"),
        null=True,
        blank=True,
        max_digits=6,
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(3000)],
        help_text="",
        )

    history = AuditTrail()

    class Meta:
        app_label = 'bcpp_subject'
        verbose_name = "PIMA CD4 count"
        verbose_name_plural = "PIMA CD4 count"
