from django.db import models
from django.core.urlresolvers import reverse
from audit_trail.audit import AuditTrail
from bhp_common.choices import YES_NO_REFUSED
from bcpp_subject.choices import NO_MEDICALCARE_REASON, HEALTH_CARE_PLACE, CARE_REGULARITY, DOCTOR_VISITS
from base_scheduled_visit_model import BaseScheduledVisitModel


class HivHealthCareCosts (BaseScheduledVisitModel):
    
    """CE001"""
    """Read to Participant: The next set of questions are about you obtaining medical or clinical care related to HIV."""
    
    hiv_medical_care = models.CharField(
        verbose_name="1. Have you ever received HIV related medical/clinical care? ",
        max_length=17,
        choices=YES_NO_REFUSED,
        help_text="",
        )
    reason_no_care = models.CharField(
        verbose_name="2. If you have never received HIV related medical/clinical care, why not? ",
        max_length=115,
        choices=NO_MEDICALCARE_REASON,
        help_text="",
        )
    place_care_received = models.CharField(
        verbose_name="3. Where do you receive most of your HIV related health care? ",
        max_length=40,
        choices=HEALTH_CARE_PLACE,
        help_text="",
        )
    care_regularity = models.CharField(
        verbose_name=("4. In the past 3 months, how many times did you obtain HIV related health care"
                      " in this location? "),
        max_length=20,
        choices=CARE_REGULARITY,
        help_text="",
        )
    doctor_visits = models.CharField(
        verbose_name="5. In the last 3 months, how often did someone take you to the doctor? ",
        max_length=32,
        choices=DOCTOR_VISITS,
        help_text="",
        )
     
    history = AuditTrail()

    def get_absolute_url(self):
        return reverse('admin:bcpp_subject_hivhealthcarecosts_change', args=(self.id,))

    class Meta:
        app_label = 'bcpp_subject'
        verbose_name = "HIV health care costs"
        verbose_name_plural = "HIV health care costs"
