from django.db import models
from bhp_common.validators import datetime_not_before_study_start, datetime_not_future, datetime_is_after_consent
from bhp_common.models import MyBasicUuidModel
from bhp_common.fields import OtherCharField
from bhp_appointment.managers import VisitManager
from appointment import Appointment


class BaseAppointmentTracking (MyBasicUuidModel):
    
    """Base model for Appt/Visit Tracking (AF002).

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
        
    
    reason = models.CharField( 
        verbose_name = "What is the reason for this visit?",
        max_length=25,
        # this is commented out and handled in the ModelForm class, see comment just below...
        #choices=VISIT_REASON,
        help_text="",
        )  
    
    """
        as each study will have variations on the 'reason' choices, allow this
        tuple to be defined at the form level. In the ModelForm add something
        like this:

        reason = forms.ChoiceField(
            label = 'Reason for visit',
            choices = [ choice for choice in VISIT_REASON ],
            help_text = "If 'unscheduled', information is usually reported at the next scheduled visit, but exceptions may arise",
            widget=AdminRadioSelect(renderer=AdminRadioFieldRenderer),
            )
        
        where the choices tuple is defined in the local app.
    """
        
    reason_missed = models.CharField(
        verbose_name = "If 'missed' above, Reason scheduled visit was missed",
        max_length = 35,
        blank = True,
        null = True,   
        )  
        
    """
        ...same as above...Something like this:
        
        info_source = forms.ChoiceField(
            label = 'Source of information',
            choices = [ choice for choice in VISIT_INFO_SOURCE ],
            widget=AdminRadioSelect(renderer=AdminRadioFieldRenderer),      
            )  
    """            

    info_source = models.CharField(
        verbose_name = "What is the main source of this information?",
        max_length=25,
        # this is commented out and handled in the ModelForm class
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
    #TODO: add next_scheduled_visit_datetime but put in checks for the window period etc.
    next_scheduled_visit_datetime = models.DateTimeField(
        verbose_name="Next scheduled visit date and time",
        validators=[
            datetime_is_after_consent,
            datetime_is_future,
            ],       
        )            
    """

    objects = VisitManager()

    def natural_key_as_dict(self):
        return {'appointment':self.appointment, }
    
    
    def save(self, *args, **kwargs):
        
        # TODO: BaseAppointmentTracking.save() is the correct place to recalculate ScheduledEntryBucket?? no
        
        return super(BaseAppointmentTracking, self).save(*args, **kwargs)
        
    class Meta:
        abstract = True 

