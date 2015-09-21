from django.db import models

from edc_base.audit_trail import AuditTrail

from bhp066.apps.bcpp.choices import YES_NO_DWTA, YES_NO, VERBALHIVRESULT_CHOICE

from .base_scheduled_visit_model import BaseScheduledVisitModel
from .subject_consent import SubjectConsent


class ClinicQuestionnaire (BaseScheduledVisitModel):

    CONSENT_MODEL = SubjectConsent

    know_hiv_status = models.CharField(
        verbose_name="Do you know your current HIV status?",
        max_length=25,
        null=True,
        blank=True,
        choices=YES_NO_DWTA,
        help_text="")

    current_hiv_status = models.CharField(
        verbose_name="Please tell me your current HIV status?",
        max_length=30,
        null=True,
        blank=True,
        choices=VERBALHIVRESULT_CHOICE,
        help_text="")

    on_arv = models.CharField(
        verbose_name="Are you currently taking antiretroviral therapy (ARVs)?",
        max_length=25,
        null=True,
        blank=True,
        choices=YES_NO_DWTA,
        help_text="")

    arv_evidence = models.CharField(
        verbose_name="Is there evidence [OPD card, tablets, masa number] that the participant is on therapy?",
        choices=YES_NO,
        null=True,
        blank=True,
        max_length=3)

    history = AuditTrail()

    class Meta:
        app_label = 'bcpp_subject'
        verbose_name = "Clinic Questionnaire"
        verbose_name_plural = "Clinic Questionnaire"
