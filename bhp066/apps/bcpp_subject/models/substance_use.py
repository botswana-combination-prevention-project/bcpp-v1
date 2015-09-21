from django.db import models

from edc_base.audit_trail import AuditTrail

from bhp066.apps.bcpp.choices import YES_NO_DWTA, ALCOHOL_CHOICE

from .base_scheduled_visit_model import BaseScheduledVisitModel
from .subject_consent import SubjectConsent


class SubstanceUse (BaseScheduledVisitModel):

    CONSENT_MODEL = SubjectConsent

    alcohol = models.CharField(
        verbose_name="In the past month, how often did you consume alcohol?",
        max_length=25,
        choices=ALCOHOL_CHOICE,
        help_text="If participant does not know exactly, ask to give a best guess.",
    )

    smoke = models.CharField(
        verbose_name="Do you currently smoke any tobacco products, such as"
                       " cigarettes, cigars, or pipes?",
        max_length=25,
        choices=YES_NO_DWTA,
        help_text="",
    )

    history = AuditTrail()

    class Meta:
        app_label = 'bcpp_subject'
        verbose_name = "Substance Use"
        verbose_name_plural = "Substance Use"
