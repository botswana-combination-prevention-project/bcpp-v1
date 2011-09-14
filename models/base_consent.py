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

class BaseConsentModel(MyBasicUuidModel):

    """infants consent models may wish to start here as they would not need the identity fields
       and the dob validators would be different from those reading values from StudySpecific
    """
     
    subject_identifier = models.CharField('Subject Identifier', 
        max_length=25, 
        unique=True, 
        help_text='', 
        )
        
    first_name = NameField(
        verbose_name = _("First name")
        )
        
    last_name = NameField(
        verbose_name = _("Last name")
    )
    
    initials = InitialsField()
    
    study_site = models.ForeignKey(StudySite,
        verbose_name = 'Site',
        help_text="This refers to the site or 'clinic area' where the subject is being consented."
        )
    consent_datetime = models.DateTimeField("Consent date and time",
        validators=[
            datetime_not_before_study_start,
            datetime_not_future,],
        )
        
    guardian_name = models.CharField(
        verbose_name = _("Guardian\'s Last and first name (minors only)"),
        max_length = 150,
        validators = [
            RegexValidator('^[A-Z]{1-50}\,[A-Z]{1-50}$', 'Invalid format. Format is \'LASTNAME, FIRSTNAME\'. All uppercase separated by a comma'),
            ],
        blank=True,
        null=True,    
        help_text = _('Required only if subject  a minor. Format is \'LASTNAME, FIRSTNAME\'. All uppercase separated by a comma'),
        )
            
    comment = models.CharField("Comment", 
        max_length=250, 
        blank=True
        )        


    class Meta:
       abstract = True
       unique_together = (("first_name", "last_name"),)
