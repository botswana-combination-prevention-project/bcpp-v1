from django.db import models
from django.core.urlresolvers import reverse
from audit_trail.audit import AuditTrail
from bcpp.choices import LENGTHRESIDENCE_CHOICE, YES_NO_DONT_ANSWER, YES_NO_UNSURE, NIGHTSAWAY_CHOICE, CATTLEPOSTLANDS_CHOICE, REASONAWAY_CHOICE 
from base_scheduled_visit_model import BaseScheduledVisitModel


class ResidencyMobility (BaseScheduledVisitModel):
    
    """CS002"""
    
    lengthresidence = models.CharField(
        verbose_name="1. How long have your lived in this community?",
        max_length=15,
        choices=LENGTHRESIDENCE_CHOICE,
        help_text="",
        )

    forteennights = models.CharField(
        verbose_name=("2. In the past 12 months, have you typically spent 14 or more nights per month"
                      " in this community? [If moved into the community in the past 12 months, "
                      "then since moving in have you typically spent 14 or more nights per month"
                      " in this household?]"),
        max_length=15,
        choices=YES_NO_DONT_ANSWER,
        help_text="",
        )

    intendresidency  = models.CharField(
        verbose_name="3. Do you intend to stay in this community for the next year?",
        max_length=15,
        choices=YES_NO_UNSURE,
        help_text="",
        )

    nightsaway = models.CharField(
        verbose_name=("4. In the past 12 months, in total how many nights did you spend away"
                      " from this community, including visits to cattle post and lands?"
                      "[If you don't know exactly, give your best guess]"),
        max_length=15,
        choices=NIGHTSAWAY_CHOICE,
        help_text="",
        )

    cattlepostlands = models.CharField(
        verbose_name=("5. In the past 12 months, during the times you were away from this community, "
                      "where were you primarily staying?"),
        max_length=15,
        null=True,
        blank=True,
        choices=CATTLEPOSTLANDS_CHOICE,
        help_text="",
        )

    reasonaway = models.CharField(
        verbose_name="6. In the past 12 months, what was the primary reason for being away from this community?",
        max_length=15,
        null=True,
        blank=True,
        choices=REASONAWAY_CHOICE,
        help_text="",
        )
    
    history = AuditTrail()

    def get_absolute_url(self):
        return reverse('admin:bcpp_subject_residencymobility_change', args=(self.id,))

    class Meta:
        app_label = 'bcpp_subject'
        verbose_name = "Residency & Mobility"
        verbose_name_plural = "Residency & Mobility"
