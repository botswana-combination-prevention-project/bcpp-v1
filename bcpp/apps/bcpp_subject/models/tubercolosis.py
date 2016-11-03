from django.db import models

from edc_base.audit_trail import AuditTrail
from edc_base.model.fields import OtherCharField
from edc_base.model.validators import date_not_future

from bhp066.apps.bcpp.choices import DXTB_CHOICE

from .base_scheduled_visit_model import BaseScheduledVisitModel
from .subject_consent import SubjectConsent


class Tubercolosis (BaseScheduledVisitModel):

    """A model completed by the user to record any diagnosis of
    Tuberculosis in the past 12 months."""

    CONSENT_MODEL = SubjectConsent

    date_tb = models.DateField(
        verbose_name="Date of the diagnosis of tuberculosis:",
        validators=[date_not_future],
        help_text="",
    )

    dx_tb = models.CharField(
        verbose_name="[Interviewer:]What is the tuberculosis diagnosis as recorded?",
        max_length=50,
        choices=DXTB_CHOICE,
        help_text="",
    )
    dx_tb_other = OtherCharField(
        null=True,
    )

    history = AuditTrail()

    class Meta:
        app_label = 'bcpp_subject'
        verbose_name = "Tubercolosis"
        verbose_name_plural = "Tubercolosis"
