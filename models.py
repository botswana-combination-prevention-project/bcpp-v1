from django.db import models
from bhp_common.models import MyBasicListModel, MyBasicUuidModel
from bhp_common.fields import OtherCharField
from bhp_common.choices import YES_NO
from bhp_common.validators import datetime_not_before_study_start, datetime_not_future

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

class Subject (MyBasicUuidModel):
       
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
        return "%s %s" % (self.subject_identifier, self.subject_type)
    
    class Meta:
        abstract=True

class RegisteredSubject(Subject):

    pass

    def __unicode__ (self):
        return "%s %s (%s)" % (self.subject_identifier, self.subject_type, self.first_name)


class RandomizedSubject(Subject):

    pass

    def __unicode__ (self):
        return "%s %s" % (self.subject_identifier, self.subject_type)

class RegistrationFormBase(MyBasicUuidModel):
    
    registered_subject = models.OneToOneField(RegisteredSubject,
        editable=False  
        )
    
    registration_datetime = models.DateTimeField("Today's date",
        validators=[
            datetime_not_before_study_start,
            datetime_not_future,])
    
    class Meta:
        abstract=True

class RandomizationFormBase(MyBasicUuidModel):
    
    randomized_subject = models.OneToOneField(RandomizedSubject,
        editable=False  
        )
    
    registration_datetime = models.DateTimeField("Today's date",
        validators=[
            datetime_not_before_study_start,
            datetime_not_future,])
    
    class Meta:
        abstract=True


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


