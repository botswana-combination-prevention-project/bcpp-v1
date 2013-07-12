from django.db import models
from django.core.urlresolvers import reverse
from audit_trail.audit import AuditTrail
from bcpp_list.models import Diagnoses
from bcpp.choices import YES_NO_UNSURE, YES_NO_DONT_ANSWER
from base_scheduled_visit_model import BaseScheduledVisitModel


class MedicalDiagnoses (BaseScheduledVisitModel):

    """CS002"""

    diagnoses = models.ManyToManyField(Diagnoses,
        verbose_name=("Do you recall or is there a record of having any of the"
                      " following serious illnesses?"),
        help_text="tick all that apply",
        )

    heart_attack_record = models.CharField(
        verbose_name=("Is a record (OPD card, discharge summary) of a heart disease or stroke"
                       " diagnosis available to review?"),
        max_length=25,
        null=True,
        blank=True,
        choices=YES_NO_DONT_ANSWER,
        help_text="Please review the available OPD card or other medical records, for all participants",
        )

    cancer_record = models.CharField(
        verbose_name="Is a record (OPD card, discharge summary) of a cancer diagnosis available to review?",
        max_length=25,
        null=True,
        blank=True,
        choices=YES_NO_DONT_ANSWER,
        help_text="Please review the available OPD card or other medical records, for all participants",
        )

    sti = models.CharField(
        verbose_name=("In the past 12 months, have you been treated for discharge from the "
                       "penis/vagina or for a sore in the genitals or sexually transmitted infection?"),
        max_length=25,
        choices=YES_NO_UNSURE,
        help_text=("Note:Common terminology includes vaginal or penile discharge, ulcer or other"
                   " sore on the genitals/anus"),
        )

    tb_record = models.CharField(
        verbose_name=("Is a record (OPD card, discharge summary, TB card) of a tuberculosis"
                       " infection available to review?"),
        max_length=25,
        null=True,
        blank=True,
        choices=YES_NO_DONT_ANSWER,
        help_text="Please review the available OPD card or other medical records, for all participants",
        )

    history = AuditTrail()

    def get_absolute_url(self):
        return reverse('admin:bcpp_subject_medicaldiagnoses_change', args=(self.id,))

    class Meta:
        app_label = 'bcpp_subject'
        verbose_name = "Medical Diagnoses"
        verbose_name_plural = "Medical Diagnoses"
