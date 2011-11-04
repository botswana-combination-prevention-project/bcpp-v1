from django.db import models
from bhp_common.models import MyBasicListModel, MyBasicUuidModel
from bhp_common.fields import OtherCharField
from bhp_common.choices import YES_NO
from bhp_code_lists.models import DxCode
from bhp_common.validators import date_not_before_study_start, date_not_future
from bhp_registration.models import BaseRegisteredSubjectModel


class DeathCauseInfo (MyBasicListModel):
    class Meta:
        ordering = ['display_index']  
        app_label = 'bhp_adverse'
                
class DeathCauseCategory (MyBasicListModel):
    class Meta:
        ordering = ['display_index']  
        app_label = 'bhp_adverse'
                
class DeathMedicalResponsibility (MyBasicListModel):
    class Meta:
        ordering = ['display_index']  
        app_label = 'bhp_adverse'        
        
class DeathReasonHospitalized (MyBasicListModel):
    class Meta:
        ordering = ['display_index']  
        app_label = 'bhp_adverse'
        
class BaseDeathReport(BaseRegisteredSubjectModel):
    
    """
    Death form / AF005
    """
    
    #registered_subject = models.OneToOneField(RegisteredSubject)
    
    death_date = models.DateField( 
        verbose_name="1. Date of Death:",
        validators = [
            date_not_before_study_start, 
            date_not_future,
            ],
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
    death_cause = models.TextField(
        max_length=1000,
        verbose_name="4. Describe the major cause of death(including pertinent autopsy information if available),starting with the first noticeable illness thought to be related to death,continuing to time of death. ",
        help_text = "Note: Cardiac and pulmonary arrest are not major reasons and should not be used to describe major cause)"  
        )    
    death_cause_category = models.ForeignKey(DeathCauseCategory, 
        verbose_name="4a. Based on the above description, what category best defines the major cause of death? ",
        help_text="",
        )   
    death_cause_other = OtherCharField(
        verbose_name="4b. if other specify...",
        blank=True,
        null=True,     
        )   
    dx_code = models.ForeignKey(DxCode,
        max_length=25,
        verbose_name="4c. Please code the cause of death as one of the following:",
        help_text="Use diagnosis code from Diagnosis Reference Listing",
        )
    illness_duration = models.IntegerField(
        verbose_name="4d. Duration of acute illness directly causing death   ",
        help_text="If unknown enter -1",
        )
    death_medical_responsibility = models.ForeignKey(DeathMedicalResponsibility, 
        verbose_name="5. Who was responsible for primary medical care of the participant during the month prior to death?",
        help_text="",
        )    
    participant_hospitalized = models.CharField(
        max_length=3,
        choices=YES_NO,
        verbose_name="6. Was the participant hospitalised before death?",
        help_text="",
        )
    death_reason_hospitalized = models.ForeignKey(DeathReasonHospitalized, 
        verbose_name="6a. if yes, hospitalized, what was the primary reason for hospitalisation? ",
        help_text="",
        blank=True,
        null=True,
        )   
    days_hospitalized = models.IntegerField(
        verbose_name="6b. if yes, hospitalized, for how many days was the participant hospitalised during the illness immediately before death? ",
        help_text="",
        default = 0,
        )
    
    comment = models.TextField(
        max_length = 500,
        verbose_name="8. Comments",
        blank=True,
        null=True,   
        ) 
        
    class Meta:
        abstract = True

