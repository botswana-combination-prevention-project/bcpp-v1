from django.db import models
from bhp_common.models import MyBasicListModel, MyBasicUuidModel
from bhp_common.fields import OtherCharField
from bhp_common.choices import YES_NO
from bhp_common.validators import datetime_not_before_study_start, datetime_not_future
from bhp_consent.models import SubjectConsent
from bhp_code_lists.models import DiagnosisCode
from choices import REGISTRATION_STATUS, SUBJECT_TYPE


class RandomizationListBase (MyBasicUuidModel):

    sid  = models.IntegerField(
        unique=True, 
        verbose_name="SID",
        )
    site_name = models.CharField("Registration Site",
        max_length=10)    
        
    site = models.IntegerField("site code"
        )    
        
    registration_datetime = models.DateTimeField("Registration Date and Time")        

    subject_identifier = models.CharField(
        max_length = 25
        )        
        
    class Meta:
        abstract = True 

"""
You might inheret from RandomizationList to get something like this, assuming your app is 'protocol'

class RandomizationList (RandomizationListBase):

    feeding_choice = models.CharField("Feeding Choice",
        max_length=2)
    haart_status = models.CharField("Maternal HAART Status",
        max_length=10)    
    rx = models.CharField("Study Drug",
        max_length=7)        
    feeding_duration = models.IntegerField("Feeding Duration in Months",)
        
    def __unicode__(self):
        return "%s %s %s (%s)" % (self.sid, self.feeding_choice,self.feeding_duration, self.haart_status)
    
    class Meta:
        app_labl='protocol'

"""

class RegisteredSubject (MyBasicUuidModel):
       
    subject_consent_id = models.CharField(max_length=100, null=True)
       
    subject_identifier = models.CharField(
        verbose_name = "Subject Identifier",
        max_length=25, 
        unique=True, 
        editable=False)
    
    first_name = models.CharField(
        max_length=50,
        )
    
    initials = models.CharField(
        max_length=3,
        )                    
    
    subject_type = models.CharField(
        max_length = 25,
        choices=SUBJECT_TYPE,
        )         
    
    screening_datetime=models.DateTimeField(
        null=True,
        blank=True
        )
    
    registration_datetime=models.DateTimeField(        
        null=True,
        blank=True
        )
    
    """ for simplicity, if going straight from screen to rando, 
        update bothe reg date and rando date """
    randomization_datetime=models.DateTimeField(
        null=True,
        blank=True
        )


    registration_status = models.CharField(
        verbose_name = "Current status",
        max_length = 25,
        choices=REGISTRATION_STATUS,
        )
    
    def __unicode__ (self):
        return "%s %s" % (self.subject_identifier, self.registration_status)



class RegistrationFormBase(MyBasicUuidModel):
    
    registered_subject = models.ForeignKey(RegisteredSubject,
        editable=False  
        )
    
    registration_datetime = models.DateTimeField("Today's date",
        validators=[
            datetime_not_before_study_start,
            datetime_not_future,])
    
    class Meta:
        abstract=True


class RegistrationFormConsentedBase(RegistrationFormBase):
    
    subject_consent = models.OneToOneField(SubjectConsent)                   
    
    class Meta:
        abstract=True

"""
    This table will be populated by a view function
    linked to one or more registration or
    randomization functions, depending on the 
    design of the protocol.
"""    



class OffStudyReason (MyBasicListModel):

    subject_type = models.CharField(
        max_length = 25,
        choices=SUBJECT_TYPE,
        )         

    class Meta:
        ordering = ['display_index'] 

"""
    Basic Off study / AF004
"""
class OffStudy(MyBasicUuidModel):

    registered_subject = models.OneToOneField(RegisteredSubject)

    off_study_date=models.DateField(
        verbose_name="Off-study Date",
        help_text="",
        )

    reason_off_study = models.ForeignKey(OffStudyReason,
        verbose_name="Please code the primary reason for why the subject is being taken off-study",
        help_text="",
        )

    reason_off_study_other = OtherCharField()

    comment = models.CharField(
        max_length=35,
        verbose_name="Comments:",
        blank=True,
        null=True,   
        )    

"""
    Death form / AF005
"""
class DeathCauseInfo (MyBasicListModel):
    class Meta:
        ordering = ['display_index']  
class DeathCauseCategory (MyBasicListModel):
    class Meta:
        ordering = ['display_index']  
class DeathMedicalResponsibility (MyBasicListModel):
    class Meta:
        ordering = ['display_index']  
class DeathReasonHospitalized (MyBasicListModel):
    class Meta:
        ordering = ['display_index']  
        
class DeathForm(MyBasicUuidModel):
    
    register_subject = models.OneToOneField(RegisteredSubject)
    
    death_date = models.DateField( 
        verbose_name="1. Date of Death:",
        help_text="",
        )   
    death_cause_info = models.ForeignKey(DeathCauseInfo, 
        verbose_name="2. What is the primary source of cause of death information? (if multiple source of information, list one with the smallest number closest to the top of the list) ",
        help_text="",
        )   
    death_cause_info_other = OtherCharField(
        verbose_name="2a. if other specify...",
        blank=True,
        null=True,     
        )   
    perform_autopsy = models.CharField(
        max_length=3,
        choices=YES_NO,
        verbose_name="3. Will an autopsy be performed later  ",
        help_text="",
        )
    death_cause = models.CharField(
        max_length=35,
        verbose_name="4.Describe the major cause of death(including pertinent autopsy information if available),starting with the first noticeable illness thought to be related to death,continuing to time of death. ",
        help_text="Note:Cardiac and pulmonary arrest are not major reasons and should not be used to describe major cause)"  
        )    
    death_cause_cat = models.ForeignKey(DeathCauseCategory, 
        verbose_name="4a. Based on the above description, what category best defines the major cause of death? ",
        help_text="",
        )   
    death_cause_other = OtherCharField(
        verbose_name="4b. if other specify...",
        blank=True,
        null=True,     
        )   
    death_cause_code = models.ForeignKey(DiagnosisCode,
        max_length=25,
        verbose_name="4c. Please code the cause of death as one of the following:",
        help_text="Use diagnosis code from Diagnosis Reference Listing",
        )
    illness_duration = models.IntegerField(
        verbose_name="4d. Duration of acute illness directly causing death   ",
        help_text="If unknown enter -1",
        )
    medical_responsibility = models.ForeignKey(DeathMedicalResponsibility, 
        verbose_name="5. Who was responsible for primary medical care of the participant during the month prior to death?",
        help_text="",
        )    
    participant_hospitalized = models.CharField(
        max_length=3,
        choices=YES_NO,
        verbose_name="6. Was the participant hospitalised before death?",
        help_text="",
        )
    reason_hospitalized = models.ForeignKey(DeathReasonHospitalized, 
        verbose_name="6a. if yes,what was the primary reason for hospitalisation? ",
        help_text="",
        )   
    days_hospitalized = models.IntegerField(
        verbose_name="6b. For how many days was the participant hospitalised during the illness immediately before death? ",
        help_text="",
        )
    
    comment = models.CharField(
        max_length=35,
        verbose_name="8.Comments",
        blank=True,
        null=True,   
        ) 
        
    def form_title (self):
        return "Death Report Form"        
        
