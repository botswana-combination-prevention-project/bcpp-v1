from django.db import models
from django.utils.translation import ugettext as _
from audit_trail.audit import AuditTrail
from bcpp_list.models import ReferredFor, ReferredTo
from base_scheduled_htc_visit import BaseScheduledHtcVisit


class Referral(BaseScheduledHtcVisit):
    
    """ Referral"""
    
    referred_for = models.ManyToManyField(ReferredFor,
        verbose_name=_("Client referred FOR:"),
        help_text='(tick all that apply)'
        )
    
    referred_to = models.ManyToManyField(ReferredTo,
        verbose_name=_("Client referred TO:"),
        help_text='(tick all that apply)',
        )
    
    history = AuditTrail()
    
    class Meta:
        app_label = 'bcpp_htc'
        verbose_name = "Referral"
        verbose_name_plural = "referral"