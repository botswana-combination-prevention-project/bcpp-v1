from django.db import models
from audit_trail.audit import AuditTrail
from bhp_base_model.fields import OtherCharField
from bcpp.choices import PLACE_CIRC, WHYCIRC_CHOICE
from bcpp_list.models import CircumcisionBenefits
from bcpp.choices import YES_NO_UNSURE
from base_scheduled_visit_model import BaseScheduledVisitModel


class Circumcised (BaseScheduledVisitModel):

    """CS002"""

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

    when_circ = models.IntegerField(
        verbose_name="At what age were you circumcised?",
        max_length=2,
        null=True,
        blank=True,
        help_text="Note:Leave blank if participant does not want to respond.",
        )

    where_circ = models.CharField(
        verbose_name="Where were you circumcised?",
        max_length=45,
        choices=PLACE_CIRC,
        null=True,
        help_text="supplemental",
        )
    where_circ_other = OtherCharField(
        null=True,
        )

    why_circ = models.CharField(
        verbose_name="What was the main reason why you were circumcised?",
        max_length=55,
        choices=WHYCIRC_CHOICE,
        null=True,
        help_text="supplemental",
        )
    why_circ_other = OtherCharField(
        null=True,
        )

    history = AuditTrail()

    class Meta:
        app_label = 'bcpp_subject'
        verbose_name = "Circumcised"
        verbose_name_plural = "Circumcised"
