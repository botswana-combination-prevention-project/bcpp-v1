from django.db import models
from django.core.validators import MinLengthValidator, MaxLengthValidator, RegexValidator
from bhp_fields.fields import MyUUIDField
from bhp_basic_models.models import MyBasicUuidModel, MyBasicModel
from bhp_choices.choices import GENDER, YES_NO, DOB_ESTIMATE
from bhp_validators.validators import dob_not_future, dob_not_today, datetime_not_future, date_not_future, datetime_not_before_study_start

class ConsentModel(MyBasicUuidModel):
    """ A consent model. The app model 'SubjectConsent' must inheret from this.
    Also, you may need to add a foreignkey field if relevant to your app. 
    For example, in the case of the 'mochudi' app,
    the consent is related to the household structure member model. The subject
    is defined in the household structure member model first and referred to
    by the consent.
    
    That is, you would add:
      
    class SubjectConsent(MyConsentModel):
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
        choices=GENDER
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
 

      

class ConsentedSubjectModel(MyBasicUuidModel):
    """All subsequent models collecting information from consented subjects
    should inheret from this model
    
    You need to add 
    
        subject_consent = models.OneToOneField(SubjectConsent)
        
    replacing 'SubjectConsent' with the model name of your consent
    
    """

    report_datetime = models.DateTimeField("Today's date",
        validators=[
            datetime_not_before_study_start,
            datetime_not_future,])

    class Meta:
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
    
