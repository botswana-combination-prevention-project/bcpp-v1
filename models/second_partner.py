from django.db import models
from django.utils.translation import ugettext as _
from audit_trail.audit import AuditTrail
from bcpp_htc.choices import RELATIONSHIP_TYPE
from base_partner import BasePartner


class SecondPartner (BasePartner):
    
    """HTC"""

    second_partner_rel = models.CharField(
        verbose_name=_("Now I am going to ask you about your second most"
                       " recent sexual partner.  What is your relationship"
                       " with this partner?"),
        choices=RELATIONSHIP_TYPE,
        max_length=45,
        help_text="",
        )

    history = AuditTrail()

    class Meta:
        app_label = 'bcpp_htc'
        verbose_name = "HTC Second Partner"
        verbose_name_plural = "HTC Second Partner"
