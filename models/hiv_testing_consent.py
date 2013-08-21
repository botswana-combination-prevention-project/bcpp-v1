from django.db import models
from django.utils.translation import ugettext as _
from audit_trail.audit import AuditTrail
from base_scheduled_htc_visit import BaseScheduledHtcVisit
from bcpp_htc.choices import REASON_NOT_TESTING
from bhp_common.choices import YES_NO


class HivTestingConsent(BaseScheduledHtcVisit): 
    
    """ HIV Testing and Counseling Consent"""
    
    testing_today = models.CharField(
        verbose_name=_("Do you consent to HIV testing and counseling today?"),
        max_length=15,
        choices=YES_NO,
        help_text='',             
        )
    
    reason_not_testing = models.CharField(
        verbose_name=_("What is the main reason you did not want HIV testing as part of today\'s visit?"),
        max_length=75,
        choices=REASON_NOT_TESTING,
        null=True,
        blank=True,
        help_text='',   
        )
    
    history = AuditTrail()
    
    class Meta:
        app_label = 'bcpp_htc'
        verbose_name = "HIV testing consent"
        verbose_name_plural = "HIV testing consent"