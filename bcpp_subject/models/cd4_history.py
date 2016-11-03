from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

from edc_base.audit_trail import AuditTrail
from edc_base.model.validators import datetime_not_future

from bhp066.apps.bcpp.choices import YES_NO

from .base_scheduled_visit_model import BaseScheduledVisitModel
from .subject_consent import SubjectConsent


class Cd4History (BaseScheduledVisitModel):

    """CS002 - used to collect participant CD4 History"""

    CONSENT_MODEL = SubjectConsent

    record_available = models.CharField(
        verbose_name="Is record of last CD4 count available?",
        max_length=3,
        choices=YES_NO,
        help_text="")

    last_cd4_count = models.DecimalField(
        verbose_name="What is the value of the last 'CD4' test recorded?",
        max_digits=6,
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(3000)],
        null=True,
        blank=True,
        help_text="")

    last_cd4_drawn_date = models.DateField(
        verbose_name="Date last 'CD4' test was run",
        validators=[
            datetime_not_future, ],
        null=True,
        blank=True,
        help_text="")

    history = AuditTrail()

    class Meta:
        app_label = 'bcpp_subject'
        verbose_name = "CD4 History"
        verbose_name_plural = "CD4 History"
