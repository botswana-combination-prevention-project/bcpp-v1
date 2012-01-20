from datetime import date
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.validators import MinLengthValidator, MaxLengthValidator, RegexValidator
from bhp_common.fields import MyUUIDField
from bhp_common.fields import NameField, InitialsField, IdentityTypeField, IsDateEstimatedField
from bhp_common.models import MyBasicUuidModel, MyBasicModel
from bhp_common.fields import OmangField
from bhp_common.choices import GENDER, YES_NO, YES_NO_DOESNT_WORK
from bhp_common.fields import OtherCharField
from bhp_common.validators import dob_not_future, dob_not_today, datetime_not_future, date_not_future, datetime_not_before_study_start
from bhp_common.validators import MinConsentAge,MaxConsentAge, GenderOfConsent
from bhp_common.validators import BWCellNumber, BWTelephoneNumber
from bhp_variables.models import StudySite


class BaseLocator(MyBasicUuidModel): 

    date_signed = models.DateField( 
        verbose_name = "1. Date Locator Form signed ",
        default = date.today(),
        help_text="",
        ) 
    mail_address = OtherCharField(
        max_length=35,
        verbose_name = "Mailing address ",
        help_text="",
        )
    care_clinic = OtherCharField(
        max_length=35,
        verbose_name = "Health clinic where your infant will receive their routine care ",
        help_text="",
        ) 
    home_visit_permission = models.CharField(
        max_length = 25,
        choices = YES_NO,
        verbose_name = "Has the participant given her permission for study staff to make home visits for follow-up purposes before and during the study?",
        )
    physical_address = models.TextField(
        max_length = 350,
        verbose_name = "Physical address with detailed description",
        blank=True,
        null=True,
        help_text="",
        ) 
    may_follow_up = models.CharField(
        max_length=25,
        choices=YES_NO,
        verbose_name="3. Has the participant given her permission for study staff to call her for follow-up purposes before and during the study?", 
        )

    subject_cell = models.IntegerField(
        max_length = 8,
        verbose_name = "Cell number",
        validators = [BWCellNumber,],
        blank=True,
        null=True,
        help_text="",
        )
    subject_cell_alt= models.IntegerField(
        max_length = 8,
        verbose_name = "Cell number (alternate)",
        validators = [BWCellNumber,],
        help_text="",
        blank=True,
        null=True,
        )
    subject_phone = models.IntegerField(
        max_length = 8,
        verbose_name = "Telephone",  
        validators = [BWTelephoneNumber,],    
        help_text="",
        blank=True,
        null=True,
        )  
        
    subject_phone_alt = models.IntegerField(
        max_length=8,
        verbose_name = "Telephone (alternate)",               
        help_text="",
        validators = [BWTelephoneNumber,],
        blank=True,
        null=True,
        )  
        
    may_call_work = models.CharField(
        max_length=25,
        choices=YES_NO_DOESNT_WORK,
        verbose_name = "Has the participant given her permission for study staff to contact her at work for follow up purposes before and during the study?", 
        help_text=" if 'No' go to section B, otherwise continue"
    )
    subject_work_place = models.TextField(
        max_length=35,
        verbose_name = "Name and location of work place",
        help_text="",
        blank=True,
        null=True,        
        )
    subject_work_phone = models.IntegerField(
        max_length=8,
        verbose_name = "Work telephone number ",               
        help_text="",
        validators = [BWTelephoneNumber,],
        blank=True,
        null=True,
        )          
    may_contact_someone = models.CharField(
        max_length=25,
        choices=YES_NO,
        verbose_name = "Has the participant given her permission for study staff to contact anyone else for follow-up purposes before and during the study?", 
        help_text = "For example a partner, spouse, family member, neighbour ...",
        )
    contact_name = OtherCharField(
        max_length=35,
        verbose_name = "Full names of the contact person",
        help_text="",
        )
    contact_rel = OtherCharField(
        max_length=35,
        verbose_name = "Relationship to participant",
        help_text="",
        
        )
    contact_physical_address = models.TextField(
        max_length=350,
        verbose_name = "Full physical address ",
        blank=True,
        null=True,
        help_text="",
        )
    contact_cell = models.IntegerField(
        max_length=8,
        verbose_name = "Cell number",
        validators = [BWCellNumber,],
        help_text="",
        blank=True,
        null=True,
        )
    contact_phone = models.IntegerField(
        max_length=8,
        verbose_name = "Telephone number",
        validators = [BWTelephoneNumber,],
        help_text="", 
        blank=True,
        null=True,   
        )

    class Meta:
        abstract=True
        
