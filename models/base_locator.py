from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.validators import MinLengthValidator, MaxLengthValidator, RegexValidator
from bhp_common.fields import MyUUIDField
from bhp_common.fields import NameField, InitialsField, IdentityTypeField, IsDateEstimatedField
from bhp_common.models import MyBasicUuidModel, MyBasicModel
from bhp_common.fields import OmangField
from bhp_common.choices import GENDER, YES_NO
from bhp_common.fields import OtherCharField
from bhp_common.validators import dob_not_future, dob_not_today, datetime_not_future, date_not_future, datetime_not_before_study_start
from bhp_common.validators import MinConsentAge,MaxConsentAge, GenderOfConsent
from bhp_common.validators import BWCellNumber, BWTelephoneNumber
from bhp_variables.models import StudySite
from mpepu_maternal.models import BaseScheduledVisitModel

class BaseLocator(BaseScheduledVisitModel): 

    date_signed = models.DateField( 
        verbose_name = "1.Date Locator Form signed ",
        help_text="",
        ) 
    mail_address = OtherCharField(
        max_length=35,
        verbose_name="1a. Mailing address ",
        help_text="",
        )
    care_clinic = OtherCharField(
        max_length=35,
        verbose_name="1b. Health clinic where your infant will receive their routine care ",
        help_text="",
        ) 
    home_visit_permission = models.CharField(
        max_length=25,
        choices=YES_NO,
        verbose_name="2. Has the participant given her permission for study staff to make home visits for follow-up purposes before and during the study?",
        help_text="if 'No' go to Question 3, otherwise continue",
        )
    physical_address = OtherCharField(
        max_length=350,
        verbose_name="2a. If yes, please provide physical address with detailed description",
        help_text="",
        ) 
    may_follow_up = models.CharField(
        max_length=25,
        choices=YES_NO,
        verbose_name="3. Has the participant given her permission for study staff to call her  for follow-up purposes before and during the study?", 
        help_text="if 'No' go to Question 4, otherwise continue",
        )
    subject_cell = models.IntegerField(
        max_length=8,
        verbose_name="3a. Cell number",
        validators = [BWCellNumber,],
        blank=True,
        null=True,
        help_text="",
        )
    subject_cell_alt= models.IntegerField(
        max_length=8,
        verbose_name="3b. Cell number (alternate)",
        validators = [BWCellNumber,],
        help_text="",
        blank=True,
        null=True,
        )
    subject_phone = models.IntegerField(
        max_length=8,
        verbose_name="3c. Telephone",  
        validators = [BWTelephoneNumber,],    
        help_text="",
        blank=True,
        null=True,
        )  
    subject_phone_alt = models.IntegerField(
        max_length=8,
        verbose_name="3d. Telephone (alternate)",               
        help_text="",
        validators = [BWTelephoneNumber,],
        blank=True,
        null=True,
        )  
    may_call_work = models.CharField(
        max_length=25,
        choices=YES_NO,
        verbose_name="4. Has the participant given her permission for study staff to contact her at work for follow up purposes before and during the study?", 
        help_text=" if 'No' go to section B, otherwise continue"
    )
    subject_work_place = OtherCharField(
        max_length=35,
        verbose_name="4a. Name and location of work place",
        help_text="",
        blank=True,
        null=True,        
        )
    subject_work_phone = models.IntegerField(
        max_length=8,
        verbose_name="4b.Work telephone number ",               
        help_text="",
        validators = [BWTelephoneNumber,],
        blank=True,
        null=True,
        )          
    may_contact_someone = models.CharField(
        max_length=25,
        choices=YES_NO,
        verbose_name="5. Has the participant given her permission for study staff to contact anyone else (e.g partner, spouse, family member, neighbour) for follow-up purposes before and during the study?", 
        help_text="",
        )
    contact_name = OtherCharField(
        max_length=35,
        verbose_name="5a.Full names of the contact person",
        help_text="",
        )
    contact_rel = OtherCharField(
        max_length=35,
        verbose_name="5b.Relationship to participant",
        help_text="",
        
        )
    contact_physical_address = OtherCharField(
        max_length=350,
        verbose_name="5c.Full physical address ",
        help_text="",
        )
    contact_cell = models.IntegerField(
        max_length=8,
        verbose_name="5d. Cell number",
        validators = [BWCellNumber,],
        help_text="",
        blank=True,
        null=True,
        )
    contact_phone = models.IntegerField(
        max_length=8,
        verbose_name="5e. Telephone number",
        validators = [BWTelephoneNumber,],
        help_text="", 
        blank=True,
        null=True,   
        )
    has_caretaker_alt = models.CharField(
        max_length=25,
        choices=YES_NO,
        verbose_name="6.Has the participant identified someone who will be responsible for the care of the baby in case of her death, to whom the study team could share information about her baby's health?", 
        help_text="",        
        )
    caretaker_name = OtherCharField(
        max_length=35,
        verbose_name="6a. Full Name of the responsible person",
        help_text="include firstname and surname",
        blank=True,
        null=True,
        )
    caretaker_cell = models.IntegerField(
        max_length=8,
        verbose_name="6b. Cell number",
        validators = [BWCellNumber,],
        help_text="",
        blank=True,
        null=True,
        )
    caretaker_tel = models.IntegerField(
        max_length=8,
        verbose_name="6c. Telephone number",
        validators = [BWTelephoneNumber,],
        help_text="",
        blank=True,
        null=True,
        ) 

    class Meta:
        abstract=True
        
