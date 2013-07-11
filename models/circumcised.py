from django.db import models
from audit_trail.audit import AuditTrail
from bhp_base_model.fields import OtherCharField  
from bcpp.choices import PLACE_CIRC, WHYCIRC_CHOICE
from base_circumcision import BaseCircumcision


class Circumcised (BaseCircumcision):

    """CS002"""

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
        help_text="supplemental",
        )
    where_circ_other = OtherCharField()

    why_circ = models.CharField(
        verbose_name="What was the main reason why you were circumcised?",
        max_length=55,
        choices=WHYCIRC_CHOICE,
        help_text="supplemental",
        )
    why_circ_other = OtherCharField()

    history = AuditTrail()

    class Meta:
        app_label = 'bcpp_subject'
        verbose_name = "Circumcised"
        verbose_name_plural = "Circumcised"
