from django.db import models
from django.utils.translation import ugettext as _
from audit_trail.audit import AuditTrail
from bcpp_htc.choices import SYMPTOMS
from bhp_common.choices import YES_NO, POS_NEG, YES_NO_DONT_KNOW
from base_scheduled_htc_visit import BaseScheduledHtcVisit


class HivResult(BaseScheduledHtcVisit):
    
    """ HIV Test Result """
    
    todays_result = models.CharField(
        verbose_name=_("Today\'s results:"),
        max_length=15,
        choices=POS_NEG,
        help_text='',
        )
    
    couples_testing = models.CharField(
        verbose_name=_("Did testing and counseling occur through couples testing today?"),
        max_length=15,
        choices=YES_NO,
        help_text='',
        )
    
    partner_id = models.CharField(
        verbose_name=_("What is the unique identification number for the other member of the couple?"),
        max_length=25,
        help_text='',
        )
    
    symptoms = models.CharField(
        verbose_name=_("Does the client currently have any of the following symptoms?"),
        max_length=75,
        choices=SYMPTOMS,
        help_text='',
        )
    
    family_tb = models.CharField(
        verbose_name=_("Have any of the client\'s family members been diagnosed with tuberculosis?"),
        max_length=15,
        choices=YES_NO_DONT_KNOW,
        help_text='',        
        )
    
    history = AuditTrail()
    
    class Meta:
        app_label = 'bcpp_htc'
        verbose_name = "HIV test result"
        verbose_name_plural = "HIV test result"