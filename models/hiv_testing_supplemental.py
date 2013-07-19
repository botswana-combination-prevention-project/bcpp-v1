from django.db import models
from django.utils.translation import ugettext as _
from audit_trail.audit import AuditTrail
from bcpp.choices import YES_NO_UNSURE
from base_scheduled_visit_model import BaseScheduledVisitModel


class HivTestingSupplemental (BaseScheduledVisitModel):

    """CS002 - BaseClass"""

    hiv_pills = models.CharField(
        verbose_name=_("Have you ever heard about treatment for"
                      " HIV with pills called antiretroviral therapy or ARVs [or HAART]?"),
        max_length=25,
        choices=YES_NO_UNSURE,
        null=True,
        help_text="supplemental",
        )

    arvs_hiv_test = models.CharField(
        verbose_name=_("Do you believe that treatment for HIV with "
                      "antiretroviral therapy (or ARVs) can help HIV-positive people"
                      " to live longer?"),
        max_length=25,
        null=True,
        choices=YES_NO_UNSURE,
        help_text="supplemental",
        )

    history = AuditTrail()

    class Meta:
        abstract = True
