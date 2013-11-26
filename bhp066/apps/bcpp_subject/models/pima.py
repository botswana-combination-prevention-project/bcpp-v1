from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator

from edc.audit.audit_trail import AuditTrail
from edc.base.model.validators import datetime_not_future
from edc.choices.common import YES_NO

from .base_scheduled_visit_model import BaseScheduledVisitModel


class Pima (BaseScheduledVisitModel):

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
        verbose_name="PIMA CD4 machine ID?",
        max_length=9,
        validators=[RegexValidator(regex='\d+', message='PIMA ID must be a two digit number.')],
        null=True,
        blank=True,
        help_text="type this id directly from the machine as labeled")

    cd4_datetime = models.DateTimeField(
        verbose_name=("PIMA CD4 Date and time"),
        validators=[datetime_not_future],
        )

    cd4_value = models.DecimalField(
        verbose_name=("PIMA CD4 count"),
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
