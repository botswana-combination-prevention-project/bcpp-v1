from django.db import models
from django.utils.translation import ugettext as _
from edc.core.audit_trail.audit import AuditTrail
from bcpp.choices import DXTB_CHOICE
from .base_scheduled_visit_model import BaseScheduledVisitModel


class Tubercolosis (BaseScheduledVisitModel):

    """CS002 - Medical Diagnoses- Tubercolosis"""

    date_tb = models.DateField(
        verbose_name=_("Date of the diagnosis of tuberculosis:"),
        help_text="",
        )

    dx_tb = models.CharField(
        verbose_name=_("[Interviewer:]What is the tuberculosis diagnosis as recorded?"),
        max_length=50,
        choices=DXTB_CHOICE,
        help_text="",
        )

    history = AuditTrail()

    class Meta:
        app_label = 'bcpp_subject'
        verbose_name = "Tubercolosis"
        verbose_name_plural = "Tubercolosis"
