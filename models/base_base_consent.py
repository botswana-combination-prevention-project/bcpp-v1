from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.validators import RegexValidator
from bhp_crypto.fields import EncryptedIdentityField
from bhp_base_model.fields import NameField, InitialsField
try:
    from bhp_sync.classes import BaseSyncModel as BaseUuidModel
except ImportError:
    from bhp_base_model.classes import BaseUuidModel
from bhp_base_model.validators import datetime_not_future, datetime_not_before_study_start
from bhp_variables.models import StudySite
from bhp_crypto.fields import EncryptedFirstnameField, EncryptedLastnameField


class BaseBaseConsentModel(BaseUuidModel):

    """infants consent models may wish to start here as they would not need the identity fields
       and the dob validators would be different from those reading values from StudySpecific
       
       Be careful, you are also bypassing the save method in base_consent!
    """
     
    first_name = EncryptedFirstnameField(
        verbose_name = _("First name"),
        max_length = 512
        )
        
    last_name = EncryptedLastnameField(
        verbose_name = _("Last name"),
        max_length = 512
    )
    
    initials = models.CharField(
        max_length = 3,
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
        
    guardian_name = EncryptedIdentityField(
        verbose_name = _("Guardian\'s Last and first name (minors only)"),
        max_length = 512,
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

