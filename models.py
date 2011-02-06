from django.db import models
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator
from bhp_common.validators import datetime_not_before_study_start, datetime_not_future, datetime_is_future, datetime_is_after_consent
from bhp_common.models import MyBasicListModel, MyBasicUuidModel
from bhp_common.fields import OtherCharField
from bhp_consent.models import SubjectConsent
from bhp_registration.models import RegisteredSubject
from choices import VISIT_INTERVAL_UNITS, APPT_STATUS

"""
List of valid visit codes and their name
"""
class VisitDefinition(MyBasicUuidModel):
    code = models.IntegerField(
        validators = [
            MinValueValidator(1000),
            MaxValueValidator(9999),
            ]
        )        
    title = models.CharField(
        verbose_name="Title",
        max_length=35,
        )
    instruction = models.TextField(
        verbose_name="Instructions",
        max_length=255,
        blank=True
        )    
    time_point = models.IntegerField(
        verbose_name = "Time point",
        )
  
    time_point_unit = models.CharField(
        max_length=15,    
        verbose_name="Units for visit intervals (default is days)",
        choices=VISIT_INTERVAL_UNITS,
        )        
    time_point_window_period_pre = models.IntegerField(
        verbose_name="Pre-visit interval of window period",
        help_text="time interval from visit time point to beginning of visit window",
        )
    time_point_window_period_post = models.IntegerField(
        verbose_name="Post-visit interval of window period",
        help_text="time interval from visit time point to end of visit window",
        )
    
    def __unicode__(self):
        return '%s: %s' % (self.code, self.title)
    
    class Meta:
        ordering = ['time_point']  


# Appointment #######################################

"""
    An appointment covers ONE VisitTrack record. 
    So the user must make an appointment before tracking the visit.
    
"""    
class Appointment (MyBasicUuidModel):

    subject_consent = models.ForeignKey(SubjectConsent) 

    appt_datetime = models.DateTimeField(
        verbose_name="Appointment date and time",
        help_text="",
        validators=[datetime_is_future,],
        )
           
    appt_status = models.CharField(
        verbose_name = "Status",
        choices=APPT_STATUS,
        max_length=25,
        )
        
    """visit_definition is the visit code plus other information"""    
    visit_definition = models.ForeignKey(VisitDefinition,
        verbose_name="Visit",
        help_text = "For tracking within the window period of a visit, use the decimal convention. Format is NNNN.N. e.g 1000.0, 1000.1, 1000.2, etc)",
        )
        
    """visit_instance should be populated by the system"""    
    visit_instance = models.IntegerField(
        verbose_name="Instance",
        validators=[
            MinValueValidator(0),
            MaxValueValidator(9),
            ],
        help_text="A decimal to represent an additional report to be included with the original visit report. (NNNN.0)",    
        )     
    

    def __unicode__(self):
        return "%s for %s [%s]" % (self.subject_consent, self.visit_definition.visit_code, self.appt_datetime, self.appt_status) 

    class Meta:
        unique_together = [('subject_consent', 'visit_definition', 'visit_instance')]

      

# VisitTracking #######################################

class VisitTrackInfoSource (MyBasicListModel):
    class Meta:
        ordering = ['display_index']  

class VisitTrackVisitReason (MyBasicListModel):
    class Meta:
        ordering = ['display_index']   

class VisitTrackSubjCurrStatus (MyBasicListModel):
    class Meta:
        ordering = ['display_index']   



"""
    This is the base class for Visit Tracking Form / AF002

    User should only be allowed to select "scheduled" appointments
"""
class VisitTrackBaseModel (MyBasicUuidModel):
    
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
        
    
    subject_current_status = models.ForeignKey(VisitTrackSubjCurrStatus,
        verbose_name = "What is the subject\'s current study status?",
        help_text = "",
        )
      
    visit_reason = models.ForeignKey(VisitTrackVisitReason, 
        verbose_name = "What is the reason for this visit?  ",
        help_text="",
        )  
        
    visit_reason_missed = models.CharField(
        verbose_name = "If 'missed' above, Reason scheduled visit was missed",
        max_length = 35,
        blank = True,
        null = True,   
        )  

    info_source = models.ForeignKey(VisitTrackInfoSource,
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

class VisitTrackReport (VisitTrackBaseModel):

    pass
    
    def __unicode__(self):
        return "%s: %s [%s]" % (self.registered_subject, self.appointment, self.visit_datetime.strftime('%Y-%m-%d'))
        
        
        

