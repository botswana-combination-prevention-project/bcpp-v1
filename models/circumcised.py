from django.db import models
from audit_trail.audit import AuditTrail
from bcpp.choices import WHERECIRC_CHOICE, WHYCIRC_CHOICE
from base_circumcision import BaseCircumcision


class Circumcised (BaseCircumcision):

    """CS002"""

    when_circ = models.IntegerField(
        verbose_name="74. At what age where you circumcised?",
        max_length=2,
        null=True,
        blank=True,
        help_text="Note:Leave blank if participant does not want to respond.",
        )

    where_circ = models.CharField(
        verbose_name="Supplemental MC10. Where were you circumcised?",
        max_length=25,
        choices=WHERECIRC_CHOICE,
        help_text="",
        )

    why_circ = models.CharField(
        verbose_name="Supplemental MC11. What was the main reason why were you circumcised?",
        max_length=25,
        choices=WHYCIRC_CHOICE,
        help_text="",
        )

    history = AuditTrail()

    class Meta:
        app_label = 'bcpp_subject'
        verbose_name = "Circumcised"
        verbose_name_plural = "Circumcised"
