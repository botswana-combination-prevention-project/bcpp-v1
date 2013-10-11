from django.db import models
from django.utils.translation import ugettext as _

from edc.audit.audit_trail import AuditTrail
from edc.choices import YES_NO_DWTA, YES_NO_UNSURE

from apps.bcpp_list.models import Diagnoses
from .base_scheduled_visit_model import BaseScheduledVisitModel


class MedicalDiagnoses (BaseScheduledVisitModel):

    """CS002"""

    diagnoses = models.ManyToManyField(Diagnoses,
        verbose_name=_("Do you recall or is there a record of having any of the"
                      " following serious illnesses?"),
        help_text="tick all that apply",
        )

    heart_attack_record = models.CharField(
        verbose_name=_("Is a record (OPD card, discharge summary) of a heart disease or stroke"
                       " diagnosis available to review?"),
        max_length=25,
        null=True,
        blank=True,
        choices=YES_NO_DWTA,
        help_text="Please review the available OPD card or other medical records, for all participants",
        )

    cancer_record = models.CharField(
        verbose_name=_("Is a record (OPD card, discharge summary) of a cancer diagnosis"
                      " available to review?"),
        max_length=25,
        null=True,
        blank=True,
        choices=YES_NO_DWTA,
        help_text="Please review the available OPD card or other medical records, for all participants",
        )

    sti_record = models.CharField(
        verbose_name=_("Is a record (OPD card, discharge summary) of a STI diagnosis"
                      " available to review?"),
        max_length=25,
        null=True,
        blank=True,
        choices=YES_NO_UNSURE,
        help_text="",
        )

    tb_record = models.CharField(
        verbose_name=_("Is a record (OPD card, discharge summary, TB card) of a tuberculosis"
                       " infection available to review?"),
        max_length=25,
        null=True,
        blank=True,
        choices=YES_NO_DWTA,
        help_text="Please review the available OPD card or other medical records, for all participants",
        )

    history = AuditTrail()

    class Meta:
        app_label = 'bcpp_subject'
        verbose_name = "Medical Diagnoses"
        verbose_name_plural = "Medical Diagnoses"
