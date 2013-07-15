from django.db import models
from bcpp_list.models import CircumcisionBenefits
from bcpp.choices import YES_NO_UNSURE
from base_scheduled_visit_model import BaseScheduledVisitModel


class BaseCircumcision (BaseScheduledVisitModel):

    circumcised = models.CharField(
        verbose_name=("Do you believe that male circumcision"
                      " has any health benefits for you?"),
        max_length=15,
        choices=YES_NO_UNSURE,
        null=True,
        help_text="supplemental",
        )

    health_benefits_smc = models.ManyToManyField(CircumcisionBenefits,
        verbose_name=("What do you believe are the health"
                      " benefits of male circumcision? (Indicate all that apply.)"),
        max_length=25,
        null=True,
        help_text="supplemental",
        )

    class Meta:
        abstract = True
