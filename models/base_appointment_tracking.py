from django.db import models
from django.core.validators import MinLengthValidator, MaxLengthValidator, RegexValidator
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator
from bhp_common.validators import datetime_not_before_study_start, datetime_not_future, datetime_is_future, datetime_is_after_consent
from bhp_common.models import MyBasicListModel, MyBasicUuidModel
from bhp_common.fields import OtherCharField
from bhp_visit.choices import SUBJECT_TYPE, VISIT_REASON, VISIT_INFO_SOURCE
from bhp_visit.models import Appointment

"""
class ApptInfoSource (MyBasicListModel):
    
    subject_type = models.CharField(
        max_length = 25,
        choices=SUBJECT_TYPE,
        )  
    class Meta:
        ordering = ['display_index']  
        app_label = 'bhp_visit'            

class ApptReason (MyBasicListModel):
    class Meta:
        ordering = ['display_index']
        app_label = 'bhp_visit'                       

class ApptCurrentStatus (MyBasicListModel):
    class Meta:
        ordering = ['display_index']   
        app_label = 'bhp_visit'                    

"""

class BaseAppointmentTracking (MyBasicUuidModel):
    
    """Base model for Appt Tracking (AF002).

    For entry, requires an appointment be created first, so there
    is no direct reference to 'registered subject' in this model.
    
    List of appointments in admin.py should be limited to scheduled
    appointments for the current registered subject. 
    
    Other ideas: ADD should only allow 'scheduled', and CHANGE only allow 'seen'
    Admin should change the status after ADD.
    
    """        

    appointment  = models.OneToOneField(Appointment)
    
    report_datetime = models.DateTimeField(
        verbose_name = "Visit Date and Time",
        validators = [
            datetime_not_before_study_start,
            datetime_is_after_consent,
            datetime_not_future,
            ],
        )
        
    
    #current_status = models.ForeignKey(ApptCurrentStatus,
    #    verbose_name = "What is the subject\'s current study status?",
    #    help_text = "",
    #    )
      
    reason = models.CharField( 
        verbose_name = "What is the reason for this visit?",
        max_length=25,
        #choices=VISIT_REASON,
        help_text="",
        )  
        
    reason_missed = models.CharField(
        verbose_name = "If 'missed' above, Reason scheduled visit was missed",
        max_length = 35,
        blank = True,
        null = True,   
        )  

    info_source = models.CharField(
        verbose_name = "What is the main source of this information?",
        max_length=25,
        #choices=VISIT_INFO_SOURCE,
        help_text="",
        )
        
    info_source_other = OtherCharField()   
        
    """
        this value should be suggested by the sytem but may be edited by the user.
        A further 'save' check should confirm that the date makes sense relative
        to the visit schedule
    """    
       
    comments = models.TextField(
        verbose_name="Comment if any additional pertinent information about the participant",
        max_length=250,
        blank=True,
        null=True,   
        )    

    """
    next_scheduled_visit_datetime = models.DateTimeField(
        verbose_name="Next scheduled visit date and time",
        validators=[
            datetime_is_after_consent,
            datetime_is_future,
            ],       
        )            
    """
        
    class Meta:
        abstract = True 

