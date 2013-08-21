from django.db import models
from django.utils.translation import ugettext as _
from audit_trail.audit import AuditTrail
from bcpp_htc.choices import REFERRED_FOR, REFERRED_TO
from base_scheduled_htc_visit import BaseScheduledHtcVisit


class Referral(BaseScheduledHtcVisit):
    
    """ Referral"""
    
    referred_for = models.CharField(
        verbose_name=_("Client referred FOR: (tick all that apply)"),
        max_length=75,
        choices=REFERRED_FOR,
        help_text=''
        )
    
    referred_to = models.CharField(
        verbose_name=_("Client referred TO: (tick all that apply)"),
        max_length=75,
        choices=REFERRED_TO,
        help_text='',
        )
    
    history = AuditTrail()
    
    class Meta:
        app_label = 'bcpp_htc'
        verbose_name = "Referral"
        verbose_name_plural = "referral"