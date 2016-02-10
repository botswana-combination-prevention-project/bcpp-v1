from django.db import models
from django.utils.translation import ugettext as _
from edc_base.audit_trail import AuditTrail
from ..choices import RELATIONSHIP_TYPE
from .base_partner import BasePartner


class HtcThirdPartner (BasePartner):

    third_partner_rel = models.CharField(
        verbose_name=_("Now I am going to ask you about your third most"
                       " recent sexual partner.  What is your relationship"
                       " with this partner?"),
        choices=RELATIONSHIP_TYPE,
        max_length=45,
        help_text="",
    )

    history = AuditTrail()

    class Meta:
        app_label = 'bcpp_htc_subject'
        verbose_name = "HTC Third Partner"
        verbose_name_plural = "HTC Third Partner"
