from django.db import models
from django.core.validators import MinLengthValidator, MaxLengthValidator, RegexValidator
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator
from bhp_common.validators import datetime_not_before_study_start, datetime_not_future, datetime_is_future, datetime_is_after_consent
from bhp_common.models import MyBasicListModel, MyBasicUuidModel
from bhp_common.fields import OtherCharField
from bhp_registration.models import RegisteredSubject
from bhp_registration.choices import SUBJECT_TYPE


class VisitTrackingInfoSource (MyBasicListModel):
    subject_type = models.CharField(
        max_length = 25,
        choices=SUBJECT_TYPE,
        )  
    class Meta:
        ordering = ['display_index']  

class VisitTrackingVisitReason (MyBasicListModel):
    class Meta:
        ordering = ['display_index']   

class VisitTrackingSubjCurrStatus (MyBasicListModel):
    class Meta:
        ordering = ['display_index']   



"""
    This is the base class for Visit Tracking Form / AF002

    User should only be allowed to select "scheduled" appointments
"""
class VisitTrackingBaseModel (MyBasicUuidModel):
    
    """
        in admin, the drop down should be limited to scheduled
        appt for the subject. Also ADD should only allow
        'scheduled', and CHANGE only allow 'seen'
        Admin should change the status after ADD.
    """        

    registered_subject = models.ForeignKey(RegisteredSubject)

    appointment  = models.OneToOneField(Appointment)
    
    visit_datetime = models.DateTimeField(
        verbose_name = "Visit Date and Time",
        validators = [
            datetime_not_before_study_start,
            datetime_is_after_consent,
            datetime_not_future,
            ],
        )
        
    
    subject_current_status = models.ForeignKey(VisitTrackingSubjCurrStatus,
        verbose_name = "What is the subject\'s current study status?",
        help_text = "",
        )
      
    visit_reason = models.ForeignKey(VisitTrackingVisitReason, 
        verbose_name = "What is the reason for this visit?  ",
        help_text="",
        )  
        
    visit_reason_missed = models.CharField(
        verbose_name = "If 'missed' above, Reason scheduled visit was missed",
        max_length = 35,
        blank = True,
        null = True,   
        )  

    info_source = models.ForeignKey(VisitTrackingInfoSource,
        verbose_name = "What is the main source of this information?",
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

    next_scheduled_visit_datetime = models.DateTimeField(
        verbose_name="Next scheduled visit date and time",
        validators=[
            datetime_is_after_consent,
            datetime_is_future,
            ],       
        )            

        
    class Meta:
        abstract = True 
        
"""
    Sample Visit Tracking Report as would be defined in your applicacation
"""    

class VisitTrackingReport (VisitTrackingBaseModel):

    pass
    
    def __unicode__(self):
        return "%s [%s] visit %s" % (self.registered_subject,self.registered_subject.initials, self.appointment.visit_definition.code )
        
        
class VisitTrackingModel(MyBasicUuidModel):

    visit_tracking_report = models.OneToOneField(VisitTrackingReport)        

    def __unicode___(self):
        return "%s" % (self.visit_tracking_report)    

    class Meta:
        abstract = True 
    
