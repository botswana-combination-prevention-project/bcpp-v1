from django.db import models
from django.utils.translation import ugettext as _
from apps.bcpp_list.models import CircumcisionBenefits
from apps.bcpp.choices import YES_NO_UNSURE
from .base_scheduled_visit_model import BaseScheduledVisitModel


class BaseCircumcision (BaseScheduledVisitModel):

    circumcised = models.CharField(
        verbose_name=_("Do you believe that male circumcision"
                      " has any health benefits for you?"),
        max_length=15,
        choices=YES_NO_UNSURE,
        null=True,
        help_text="supplemental",
        )

    health_benefits_smc = models.ManyToManyField(CircumcisionBenefits,
        verbose_name=_("What do you believe are the health"
                      " benefits of male circumcision? (Indicate all that apply.)"),
        null=True,
        blank=True,
        help_text="supplemental",
        )

    class Meta:
        abstract = True
