from django.db import models
from audit_trail.audit import AuditTrail
from bcpp.choices import LOWESTCD4_CHOICE
from base_scheduled_visit_model import BaseScheduledVisitModel


class HivMedicalCare (BaseScheduledVisitModel):

    """CS002"""

    first_hiv_care_pos = models.DateField(
        verbose_name=("When did you first receive HIV-related medical care "
                      "for such things as a CD4 count (masole), IDCC/ PMTCT"
                      " registration, additional clinic-based counseling?"),
        max_length=25,
        help_text=("Note: If participant does not want to answer, leave blank.  "
                   "If participant is unable to estimate date, leave blank."),
        )

    last_hiv_care_pos = models.DateField(
        verbose_name=("When did you last (most recently) receive HIV-related"
                      "medical care for such things as a CD4 count (masole), "
                      "IDCC/ PMTCT registration, additional clinic-based counseling?"),
        max_length=25,
        help_text=("Note: If participant does not want to answer,leave blank. "
                   "If participant is unable to estimate date, leave blank."),
        )

    lowest_cd4 = models.CharField(
        verbose_name="What was your lowest CD4 (masole) count that was ever measured?",
        max_length=25,
        choices=LOWESTCD4_CHOICE,
        help_text=("Assist the participant by helping review their outpatient cards if "
                   "they are available."),
        )

    history = AuditTrail()

    class Meta:
        app_label = 'bcpp_subject'
        verbose_name = "HIV Medical care"
        verbose_name_plural = "HIV Medical care"
