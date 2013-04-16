from django.db import models
from django.core.urlresolvers import reverse
from audit_trail.audit import AuditTrail
from bhp_common.choices import YES_NO_REFUSED
from bcpp_subject.choices import CARE_REASON, TRAVEL_HOURS
from base_scheduled_visit_model import BaseScheduledVisitModel


class HospitalAdmission (BaseScheduledVisitModel):
    
    """CE001- Resource Utilization sub"""
    
    admission_nights = models.IntegerField (
        verbose_name="16. How many total nights did you spend in the hospital in the past 3 months? ",
        max_length=2,
        null=True,
        blank=True,
        help_text="Note:If participant does not want to answer, leave blank",
        )
    reason_hospitalized = models.CharField (
        verbose_name="17. What was the primary reason for the most recent hospitalization in the past 3 months?",
        max_length=95,
        choices=CARE_REASON,
        help_text=" ",
        )
    facility_hospitalized = models.CharField (
        verbose_name="18. For this most recent hospitalization, where were you hospitalized? ",
        max_length=30,
        help_text=" ",
        )
    nights_hospitalized = models.IntegerField (
        verbose_name="19. For this most recent hospitization, how many nights total did you spend in the hospital? ",
        max_length=2,
        help_text=" ",
        )
    healthcare_expense = models.DecimalField (
        verbose_name="20. How much did you have to pay to the healthcare provider for the entire stay, including any medicines? ",
        max_digits=5,
        decimal_places=2,
        help_text="Pula",
        )
    travel_hours = models.CharField (
        verbose_name="21. For this most recent hospitalization, how long did it take you to get to the hospital? ",
        max_length=20,
        choices=TRAVEL_HOURS,
        help_text=" ",
        )
    total_expenses = models.DecimalField (
        verbose_name=("22. For this most recent hospitalization, how much did you have to pay for transport,"
                      " food and accommodation, including fuel if you used your own car? "),
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Note:If participant does not want to answer, leave blank. Currency is Pula",
        )
    hospitalization_costs = models.CharField (
        verbose_name=("23. For this most recent hospitalization, were any of these costs by covered by"
                      " anyone else, such as your medical aid or employer? "),
        max_length=17,
        choices=YES_NO_REFUSED,
        help_text=" ",
        )
    
    history = AuditTrail()

    def get_absolute_url(self):
        return reverse('admin:bcpp_subject_hospitaladmission_change', args=(self.id,))

    class Meta:
        app_label = 'bcpp_subject'
        verbose_name = "RU: Hospital Admission"
        verbose_name_plural = "RU: Hospital Admission"
