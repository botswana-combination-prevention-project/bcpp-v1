from django.db import models
from django.utils.translation import ugettext as _
from edc_core.audit_trail.audit import AuditTrail
from ..choices import STI_DX
from .base_scheduled_visit_model import BaseScheduledVisitModel


class Sti (BaseScheduledVisitModel):

    """CS002 - Medical Diagnoses - Sti"""

    sti_date = models.DateField(
        verbose_name=_("Date of the diagnosis of the STI (Sexually transmitted infection):"),
        help_text="",
        )

    sti_dx = models.CharField(
        verbose_name=_("[Interviewer:] What is the STI diagnosed as recorded?"),
        max_length=65,
        choices=STI_DX,
        help_text="",
        )

    comments = models.CharField(
        verbose_name=_("Comments"),
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
