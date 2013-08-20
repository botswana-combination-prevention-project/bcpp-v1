from django.db import models
from django.utils.translation import ugettext as _
from audit_trail.audit import AuditTrail
from bcpp_htc.choices import REASON_NOT_TESTING, SYMPTOMS, REFFERED_FOR, REFFERED_TO
from bhp_common.choices import YES_NO, POS_NEG, YES_NO_DONT_KNOW
from bcpp_subject.models.base_scheduled_visit_model import BaseScheduledVisitModel
from bhp_base_model.validators import date_not_future

class HivTestingCounseling(BaseScheduledVisitModel):
    """ F. HIV Testing and Counseling """
    
    testing_today=models.CharField(
        verbose_name=_("Do you consent to HIV testing and counseling today?"),
        max_length=15,
        choices=YES_NO,
        help_text='',             
    )
    
    reason_not_testing = models.CharField(
        verbose_name=_("What is the main reason you did not want HIV testing as part of today’s visit?"),
        max_length=75,
        choices=REASON_NOT_TESTING,
        help_text='',   
    )
    
    todays_result=models.CharField(
        verbose_name=_("Today’s results:"),
        max_length=15,
        choices=POS_NEG,
        help_text='',
    )
    
    cd4_test_date=models.DateField(
        verbose_name=_("Date CD4 test performed"),
        validators=[date_not_future],
        null=True,
        blank=False,
        help_text=_("Format is YYYY-MM-DD"),
    )
    
    cd4_result = models.CharField(
        verbose_name=_("CD4 Test Result"),
        max_length=4,
        help_text='',
    )
    
    clinic=models.CharField(
        verbose_name=_("Name of clinic referred to"),
        max_length=75,
        help_text='',
    )
    
    appointment_date=models.DateField(
        verbose_name=_("Appointment date"),
        validators=[date_not_future],
        null=True,
        blank=False,
        help_text=_("Format is YYYY-MM-DD"),
    )
    
    circumcision_ap=models.CharField(
        verbose_name=_("Was a male circumcision appointment made?"),
        max_length=15,
        choices=YES_NO,
        help_text='',    
    )
    
    circumcision_ap_date=models.DateField(
        verbose_name=_("Male circumcision appointment date"),
        validators=[date_not_future],
        null=True,
        blank=False,
        help_text=_("Format is YYYY-MM-DD"),
    )
    
    couples_testing=models.CharField(
        verbose_name=_("Did testing and counseling occur through couples testing today?"),
        max_length=15,
        choices=YES_NO,
        help_text='',
    )
    
    partner_id=models.CharField(
        verbose_name=_("What is the unique identification number for the other member of the couple?"),
        max_length=25,
        help_text='',
    )
    
    symptoms=models.CharField(
        verbose_name=_("Does the client currently have any of the following symptoms?"),
        max_length=75,
        choices=SYMPTOMS,
        help_text='',
    )
    
    family_tb=models.CharField(
        verbose_name=_("Have any of the client’s family members been diagnosed with tuberculosis?"),
        max_lenth=15,
        choices=YES_NO_DONT_KNOW,
        help_text='',        
    )
    
    reffered_for=models.CharField(
        verbose_name=_("Client referred FOR: (tick all that apply)"),
        max_length=75,
        choices=REFFERED_FOR,
        help_text=''
    )
    
    reffered_to=models.CharField(
        verbose_name=_("Client referred TO: (tick all that apply)"),
        max_length=75,
        choices=REFFERED_TO,
        help_text='',
    )
    
    history = AuditTrail()
    
    class Meta:
        app_label = 'bcpp_htc'
        verbose_name = "HIV testing and counseling"
        verbose_name_plural = "HIV testing and counseling"
    