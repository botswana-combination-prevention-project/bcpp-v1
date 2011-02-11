from django.db import models
from django.core.validators import MinLengthValidator, MaxLengthValidator, RegexValidator
from bhp_common.fields import MyUUIDField
from bhp_common.models import MyBasicUuidModel, MyBasicModel
from bhp_common.choices import GENDER, YES_NO, DOB_ESTIMATE
from bhp_common.fields import OtherCharField
from bhp_common.validators import dob_not_future, dob_not_today, datetime_not_future, date_not_future, datetime_not_before_study_start
from bhp_common.validators import MinConsentAge,MaxConsentAge, GenderOfConsent
from bhp_common.validators import BWCellNumber, BWTelephoneNumber
from bhp_variables.models import StudySite

class ConsentModel(MyBasicUuidModel):
    """ A consent model. The app model 'SubjectConsent' must inheret from this.
    Also, you may need to add a foreignkey field if relevant to your app. 
    For example, in the case of the 'mochudi' app,
    the consent is related to the household structure member model. The subject
    is defined in the household structure member model first and referred to
    by the consent.
    
    That is, you would add:
      
    class SubjectConsent(ConsentModel):
        household_structure_member = models.OneToOneField(HouseholdStructureMember)
        class Meta:
            app_label = 'mochudi'

    as the first line to the child model. 
    
    You also need to add DOB with a validator for the age 
    restriction on the consent

    dob = models.DateField('Date of birth',
        validators = [
            dob_not_future, 
            dob_not_today,
            dob_gt_eg_18],
        help_text="Format is YYYY-MM-DD",
        )
    
    
    """
    
    subject_identifier = models.CharField('Subject Identifier', 
        max_length=25, 
        unique=True, 
        help_text='Subject ID from barcode', 
        )
    first_name = models.CharField(
        verbose_name='First name', 
        max_length=250, 
        help_text="First name should match first name as recorded previously",
        validators = [
            RegexValidator("^[a-zA-Z]{1,250}$", "Ensure first name does not contain any spaces or numbers"),
            RegexValidator("^[A-Z]{1,250}$", "Ensure first name is in uppercase"),],
        )
    last_name = models.CharField(
        verbose_name='Last name', 
        max_length=250,
        validators = [
            RegexValidator("^[a-zA-Z]{1,250}$", "Ensure last name does not contain any spaces or numbers"),
            RegexValidator("^[A-Z]{1,250}$", "Ensure last name is in uppercase"),],
        )
    dob = models.DateField('Date of birth',
        validators = [
            dob_not_future, 
            dob_not_today,
            MinConsentAge,
            MaxConsentAge,            
            ],
        help_text="Format is YYYY-MM-DD",
        )
    omang = models.CharField(
        verbose_name='Identity number (OMANG, etc)', 
        max_length=250, 
        unique=True,
        help_text="Use Omang, Passport number, driver's license number or Omang receipt number"
        )
    initials = models.CharField("Initials", 
        max_length=3, 
        help_text="Format as uppercase. Initials should match initals those recorded previously",
        validators=[
            MinLengthValidator(2),
            MaxLengthValidator(3), 
            RegexValidator("^[A-Z]{1,4}$", "Ensure initials are in uppercase"),],
        )
    study_site = models.ForeignKey(StudySite,
        verbose_name = 'Site',
        help_text="This refers to the site or 'clinic area' where the subject is being consented."
        )
    consent_datetime = models.DateTimeField("Consent date and time",
        validators=[
            datetime_not_before_study_start,
            datetime_not_future,],
        )
    may_store_samples = models.CharField("Sample storage",
        max_length=3, 
        choices=YES_NO, 
        help_text="Does the subject agree to have samples stored after the study has ended"
        )
    gender = models.CharField('Gender',
        max_length=1, 
        choices=GENDER,
        validators=[
            GenderOfConsent,
            ]
        )
    #dob = models.DateField('Date of birth',
    #    validators = [
    #        dob_not_future, 
    #        dob_not_today,],
    #    help_text="Format is YYYY-MM-DD",
    #    )
    is_dob_estimated = models.CharField(
        max_length=25,
        choices=DOB_ESTIMATE,
        verbose_name="Is the subject's date of birth estimated?",
        help_text="If the subject does not know their exact date of birth, please indicate which part of the date of birth was estimated.",
        )
    comment = models.CharField("Comment", 
        max_length=250, 
        blank=True
        )

    def __unicode__(self):
        return unicode(self.subject_identifier)

    class Meta:
        unique_together = (("first_name", "last_name", "dob"),)
        ordering = ['-created']
        abstract = True
 

class SubjectIdentifierAuditTrail(MyBasicModel):
    """
    A table to track every attempt to allocate a subject identifier
    to a consented subject 'by this device'. If a subject consent is deleted
    the record in this table remains. So this is not a master list of
    valid identifiers. 
    See also AllocateSubjectIdentifier()
    """
    subject_consent_id = MyUUIDField()
    subject_identifier = models.CharField(max_length=25)
    first_name = models.CharField(max_length=250) 
    initials = models.CharField(max_length=3)
    date_allocated = models.DateTimeField()
    
    def __unicode__(self):
        return self.subject_identifier
        
    class Meta:
        ordering = ['-date_allocated']


class LocatorFormBaseModel(MyBasicUuidModel): 
    

    date_signed = models.DateField( 
        verbose_name="1.Date Locator Form signed ",
        help_text="",
        ) 
    mail_address = OtherCharField(
        max_length=35,
        verbose_name="1e. Mailing address ",
        help_text="",
        )
    care_clinic = OtherCharField(
        max_length=35,
        verbose_name="1f. Health clinic where your infant will receive their routine care ",
        help_text="",
        ) 
    home_visit_permission = models.CharField(
        max_length=25,
        choices=YES_NO,
        verbose_name="2. Has the participant given her permission for study stuff to make home visits for follow-up purposes before and during the study?",
        help_text="if 'No' go to Question 3, otherwise continue",
        )
    physical_address = OtherCharField(
        max_length=50,
        verbose_name="2a. If yes, please provide physical address with detailed description",
        help_text="",
        ) 
    may_follow_up = models.CharField(
        max_length=25,
        choices=YES_NO,
        verbose_name="3. Has the participant given her permission for study stuff to call her  for follow-up purposes before and during the study?", 
        help_text="if 'No' go to Question 4, otherwise continue",
        )
    subject_cell = models.IntegerField(
        max_length=8,
        verbose_name="3a. Cell number",
        validators = [BWCellNumber,],
        help_text="",
        )
    subject_cell_alt= models.IntegerField(
        max_length=8,
        verbose_name="3b. Cell number (alternate)",
        validators = [BWCellNumber,],
        help_text="",
        )
    subject_phone = models.IntegerField(
        max_length=8,
        verbose_name="3c. Telephone",
        validators = [BWTelephoneNumber,],        
        help_text="",
        )  
    subject_phone_alt = models.IntegerField(
        max_length=8,
        verbose_name="3d. Telephone (alternate)",
        validators = [BWTelephoneNumber,],                
        help_text="",
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
        )
    may_contact_someone = models.CharField(
        max_length=25,
        choices=YES_NO,
        verbose_name="1. Has the participant given her permission for study staff to contact anyone else (e.g partner, spouse, family member, neighbour) for follow-up purposes before and during the study?", 
        help_text="",
        )
    contact_name = OtherCharField(
        max_length=35,
        verbose_name="1a.Full names of the contact person",
        help_text="",
        )
    contact_rel = OtherCharField(
        max_length=35,
        verbose_name="1b.Relationship to participant",
        help_text="",
        )
    contact_physical_address = OtherCharField(
        max_length=35,
        verbose_name="1c.Full physical address ",
        help_text="",
        )
    contact_cell = models.IntegerField(
        max_length=8,
        verbose_name="1d. Cell number",
        help_text="",
        )
    contact_phone = models.IntegerField(
        max_length=8,
        verbose_name="1e. Telephone number",
        help_text="",
        )
    has_caretaker_alt = models.CharField(
        max_length=25,
        choices=YES_NO,
        verbose_name="2.Has the participant identified someone who will be responsible for the care of the baby in case of her death, to whom the study team could share information about her baby's health?", 
        help_text=""
        )
    caretaker_name = OtherCharField(
        max_length=35,
        verbose_name="2a. Full Name of the responsible person",
        help_text="include firstname and surname",
        )
    caretaker_cell = models.IntegerField(
        max_length=8,
        verbose_name="2b. Cell number",
        help_text="",
        )
    caretaker_tel = models.IntegerField(
        max_length=8,
        verbose_name="2c. Telephone number",
        help_text="",
        ) 

    class Meta:
        abstract=True
        
  
