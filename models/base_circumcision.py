from django.db import models
from bcpp_list.models import CicumcisionBenefits
from bcpp.choices import YES_NO_UNSURE
from base_scheduled_visit_model import BaseScheduledVisitModel


class BaseCircumcision (BaseScheduledVisitModel):
    
    """CS002"""
    
    circumcised = models.CharField(
        verbose_name = "Supplemental MC1. Do you believe that male circumcision has any health benefits for you?",
        max_length = 15,
        choices = YES_NO_UNSURE,
        help_text="",
        )
    
    healthbenefitsSMC = models.ManyToManyField(CicumcisionBenefits,
        verbose_name = "Supplemental MC2. What do you believe are the health benefits of male circumcision?",
        max_length = 25,
        help_text="Indicate all that apply.",
        )

    class Meta:
        abstract = True
