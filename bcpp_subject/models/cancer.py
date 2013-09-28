from django.db import models
from edc_lib.audit_trail.audit import AuditTrail
from bcpp.choices import DXCANCER_CHOICE
from base_scheduled_visit_model import BaseScheduledVisitModel


class Cancer (BaseScheduledVisitModel):

    """CS002 - Medical Diagnoses - Cancer"""

    date_cancer = models.DateField(
        verbose_name="Date of the diagnosis of cancer:",
        help_text="",
        )

    dx_cancer = models.CharField(
        verbose_name="[Interviewer:] What is the cancer diagnosis as recorded?",
        max_length=45,
        choices=DXCANCER_CHOICE,
        help_text="",
        )

    history = AuditTrail()

    class Meta:
        app_label = 'bcpp_subject'
        verbose_name = "Cancer"
        verbose_name_plural = "Cancer"
