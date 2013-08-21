from django.db import models
from django.utils.translation import ugettext as _
from audit_trail.audit import AuditTrail
from base_scheduled_htc_visit import BaseScheduledHtcVisit
from bhp_base_model.validators import date_not_future



class CD4Test(BaseScheduledHtcVisit):
    
    
    """ CD4 test """
    
    cd4_test_date=models.DateField(
        verbose_name=_("Date CD4 test performed"),
        validators=[date_not_future],
        help_text=_("Format is YYYY-MM-DD"),
        )
    
    cd4_result = models.CharField(
        verbose_name=_("CD4 Test Result"),
        max_length=4,
        help_text='',
    )
    
    referral_clinic = models.CharField(
        verbose_name=_("Name of clinic referred to"),
        max_length=75,
        help_text='',
        )
    
    appointment_date = models.DateField(
        verbose_name=_("Appointment date"),
        validators=[date_not_future],
        help_text=_("Format is YYYY-MM-DD"),
        )
    
    history = AuditTrail()
    
    class Meta:
        app_label = 'bcpp_htc'
        verbose_name = "CD4 Test"
        verbose_name_plural = "CD4 Test"