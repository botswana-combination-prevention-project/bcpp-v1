from datetime import date
from django.db import models
from bhp_base_model.classes import BaseUuidModel
from bhp_common.choices import YES_NO, YES_NO_DOESNT_WORK
from bhp_base_model.fields import OtherCharField
from bhp_base_model.validators import BWCellNumber, BWTelephoneNumber


class BaseLocator(BaseUuidModel): 

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
    '''
    care_clinic = OtherCharField(
        max_length=35,
        verbose_name = "Health clinic where your infant will receive their routine care ",
        help_text="",
        ) 
    '''
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
        
