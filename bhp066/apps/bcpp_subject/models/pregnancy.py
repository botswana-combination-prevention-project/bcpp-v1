from django.db import models

from edc_base.audit_trail import AuditTrail
from edc.base.model.validators import date_not_future

from bhp066.apps.bcpp.choices import ANCREG_CHOICE

from .base_pregnancy import BasePregnancy
from .subject_consent import SubjectConsent


class Pregnancy (BasePregnancy):

    """A model completed by the user for pregnant participants."""

    CONSENT_MODEL = SubjectConsent

    anc_reg = models.CharField(
        verbose_name="Have you registered for antenatal care?",
        max_length=55,
        null=True,
        blank=True,
        choices=ANCREG_CHOICE,
        help_text="",
    )

    lnmp = models.DateField(
        verbose_name="When was the first day of your last normal menstrual period?",
        validators=[date_not_future],
        help_text="",
    )

    history = AuditTrail()

    class Meta:
        app_label = 'bcpp_subject'
        verbose_name = "Pregnancy"
        verbose_name_plural = "Pregnancy"
