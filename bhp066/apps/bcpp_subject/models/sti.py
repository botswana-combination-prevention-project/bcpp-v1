from django.db import models

from edc.audit.audit_trail import AuditTrail
from edc.base.model.validators import date_not_future

from ..choices import STI_DX
from .base_scheduled_visit_model import BaseScheduledVisitModel


class Sti (BaseScheduledVisitModel):

    """CS002 - Medical Diagnoses - Sti"""

    sti_date = models.DateField(
        verbose_name=("Date of the diagnosis of the STI (Sexually transmitted infection):"),
        validators=[date_not_future],
        help_text="",
        )

    sti_dx = models.CharField(
        verbose_name=("[Interviewer:] What is the STI diagnosed as recorded?"),
        max_length=65,
        choices=STI_DX,
        help_text="",
        )

    comments = models.CharField(
        verbose_name=("Comments"),
        max_length=250,
        null=True,
        blank=True,
        help_text="",
        )

    history = AuditTrail()

    class Meta:
        app_label = 'bcpp_subject'
        verbose_name = "STI\'s"
        verbose_name_plural = "STI\'s"
