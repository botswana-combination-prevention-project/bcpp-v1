from django.db import models
from django.core.urlresolvers import reverse
from audit_trail.audit import AuditTrail
from bcpp.choices import YES_NO_UNSURE, YES_NO_DONT_ANSWER, DXHEARTATTACK_CHOICE, DXCANCER_CHOICE, DXTB_CHOICE   
from base_scheduled_visit_model import BaseScheduledVisitModel


class MedicalDiagnoses (BaseScheduledVisitModel):
    
    """CS002"""
    
    heartattack = models.CharField(
        verbose_name = "86. In the past 12 months, have you been told that you had heart disease or a stroke?",
        max_length = 15,
        choices = YES_NO_UNSURE,
        help_text="",
        )

    heartattackrecord = models.CharField(
        verbose_name =("87. Is a record (OPD card, discharge summary) of a heart disease or stroke"
                       " diagnosis available to review?"),
        max_length = 15,
        choices = YES_NO_DONT_ANSWER,
        help_text="",
        )

    dateheartattack = models.DateTimeField(
        verbose_name = "88. Date of the heart disease or stroke diagnosis:",
        max_length = 25,
        null=True, 
        blank=True,
        help_text=("Note:Record date of first day of hospital admission or date the diagnosis"
                   " was documented in the OPD record. If report not available, then record "
                   "participant's best knowledge. If participant does not want to answer,leav blank."
                   "  If unable to estimate date, record -4."),
        )

    dxheartattack = models.CharField(
        verbose_name = "89. [Interviewer:]What is the heart disease or stroke diagnosis as recorded?",
        max_length = 15,
        choices = DXHEARTATTACK_CHOICE,
        help_text="Note: If record of diagnosis is not available, record the participant's best knowledge.",
        )

    cancer = models.CharField(
        verbose_name = "90. In the past 12 months, have you been told that you have cancer?",
        max_length = 15,
        choices = YES_NO_UNSURE,
        help_text="",
        )

    cancerrecord = models.CharField(
        verbose_name = "91. Is a record (OPD card, discharge summary) of a cancer diagnosis available to review?",
        max_length = 15,
        choices = YES_NO_DONT_ANSWER,
        help_text="",
        )

    datecancer = models.DateTimeField(
        verbose_name = "92. Date of the diagnosis of cancer:",
        max_length = 25,
        null=True, 
        blank=True,
        help_text=("Note:Record date the diagnosis was documented in the OPD record"
                   " or the date of the pathology report. If report not available, "
                   "then record participant's best knowledge. If participant does not want to answer,"
                    "leave blank.  If unable to estimate date, record -4.."),
        )

    dxcancer = models.CharField(
        verbose_name = "93. [Interviewer:] What is the cancer diagnosis as recorded?",
        max_length = 15,
        choices = DXCANCER_CHOICE,
        help_text="Note: If record of diagnosis is not available, record the participant's best knowledge.",
        )

    sti = models.CharField(
        verbose_name =("94. In the past 12 months, have you been treated for discharge from the "
                       "penis/vagina or for a sore in the genitals or sexually transmitted infection?"),
        max_length = 15,
        choices = YES_NO_UNSURE,
        help_text=("Note:Common terminology includes vaginal or penile discharge, ulcer or other"
                   " sore on the genitals/anus"),
        )

    tb = models.CharField(
        verbose_name =("95. In the past 12 months, have you been told that you have active tuberculosis"
                       " [not latent/sleeping/inactive tuberculosis]?"),
        max_length = 15,
        choices = YES_NO_UNSURE,
        help_text="",
        )

    tbrecord = models.CharField(
        verbose_name =("96. Is a record (OPD card, discharge summary, TB card) of a tuberculosis"
                       " infection available to review?"),
        max_length = 15,
        choices = YES_NO_DONT_ANSWER,
        help_text="",
        )

    datetb = models.DateTimeField(
        verbose_name = "97. Date of the diagnosis of tuberculosis:",
        max_length = 25,
        null=True, 
        blank=True,
        help_text=("Note:Record date the diagnosis was documented in the OPD record or"
                   " the date of the pathology report.  If report not available, then "
                   "record participant's best knowledge. Enter -8 if participant does not"
                   " want to respond."),
        )

    dxTB = models.CharField(
        verbose_name = "98. [Interviewer:]What is the tuberculosis diagnosis as recorded?",
        max_length = 15,
        choices = DXTB_CHOICE,
        help_text="Note: If record of diagnosis is not available, record the participant's best knowledge.",
        )
    
    history = AuditTrail()

    def get_absolute_url(self):
        return reverse('admin:bcpp_subject_medicaldiagnoses_change', args=(self.id,))

    class Meta:
        app_label = 'bcpp_subject'
        verbose_name = "Medical Diagnoses"
        verbose_name_plural = "Medical Diagnoses"
