from django.db import models
from django.utils.translation import ugettext as _

from edc.audit.audit_trail import AuditTrail

from apps.bcpp.choices import YES_NO_REFUSED

from ..choices import NO_MEDICALCARE_REASON, HEALTH_CARE_PLACE, CARE_REGULARITY, DOCTOR_VISITS

from .base_scheduled_visit_model import BaseScheduledVisitModel


class HivHealthCareCosts (BaseScheduledVisitModel):

    """CE001.

    Read to Participant: The next set of questions are about you obtaining medical or clinical care related to HIV."""

    hiv_medical_care = models.CharField(
        verbose_name=_("Have you ever received HIV related medical/clinical care? "),
        max_length=17,
        choices=YES_NO_REFUSED,
        help_text="",
        )
    reason_no_care = models.CharField(
        verbose_name=_("If you have never received HIV related medical/clinical care, why not? "),
        max_length=115,
        null=True,
        blank=True,
        choices=NO_MEDICALCARE_REASON,
        help_text="",
        )
    place_care_received = models.CharField(
        verbose_name=_("Where do you receive most of your HIV related health care when not staying in the hospital? "),
        max_length=40,
        choices=HEALTH_CARE_PLACE,
        help_text="",
        )
    care_regularity = models.CharField(
        verbose_name=_("In the past 3 months, how many times did you have clinic visits to see a health care worker,"
                      " a nurse, or doctor? "),
        max_length=20,
        choices=CARE_REGULARITY,
        help_text="Do not include medicine re-fill visits.",
        )
    doctor_visits = models.CharField(
        verbose_name=_("In the last 3 months, how often did someone take you to the doctor? "),
        max_length=32,
        choices=DOCTOR_VISITS,
        help_text="",
        )

    history = AuditTrail()

    class Meta:
        app_label = 'bcpp_subject'
        verbose_name = "HIV health care costs"
        verbose_name_plural = "HIV health care costs"
