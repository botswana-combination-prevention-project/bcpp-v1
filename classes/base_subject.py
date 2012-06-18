from django.db import models
#from django.db import IntegrityError
from django.forms import ValidationError 
from django.utils.translation import ugettext_lazy as _
from django.core.validators import RegexValidator
try:
    from bhp_sync.classes import BaseSyncModel as BaseUuidModel
except ImportError:
    from bhp_base_model.classes import BaseUuidModel
from bhp_base_model.validators import dob_not_future, MinConsentAge, MaxConsentAge
from bhp_common.choices import GENDER_UNDETERMINED
from bhp_base_model.fields import IsDateEstimatedField
from bhp_crypto.fields import EncryptedFirstnameField, EncryptedLastnameField


class BaseSubject (BaseUuidModel):

    # may be null so uniqueness is enforce in save() if not null
    subject_identifier = models.CharField(
        verbose_name = "Subject Identifier",
        max_length=36, 
        null = True, 
        blank = True,
        db_index=True,               
        )
    
    first_name = EncryptedFirstnameField()
    
    last_name = EncryptedLastnameField(
        verbose_name = "Last name",
        )
    
    initials = models.CharField(
        max_length=3,
        validators = [RegexValidator(regex=r'^[A-Z]{2,3}$', 
                                    message='Ensure initials consist of letters only in upper case, no spaces.'),]
        )

    dob = models.DateField(
        verbose_name = _("Date of birth"),
        validators = [
            dob_not_future, 
            MinConsentAge,
            MaxConsentAge,            
            ],
        null = True,
        blank = False,
        help_text=_("Format is YYYY-MM-DD"),
        )

    is_dob_estimated = IsDateEstimatedField( 
        verbose_name=_("Is date of birth estimated?"),       
        null=True,
        blank=False,
        )    

    gender = models.CharField(
        verbose_name = "Gender",
        choices = GENDER_UNDETERMINED,
        max_length=1, 
        null = True,
        blank = False,
        )
    
    subject_type = models.CharField(
        max_length = 25,
        default = 'undetermined',
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
        update both registration date and randomization date """
    randomization_datetime=models.DateTimeField(
        null=True,
        blank=True
        )


    registration_status = models.CharField(
        verbose_name = "Registration status",
        max_length = 25,
        #choices=REGISTRATION_STATUS,
        null = True,
        blank = True,
        )
    
    def save(self, *args, **kwargs):
        # for new instances, enforce unique subject_identifier if not null
        if not self.pk and self.subject_identifier:
            if self.__class__.objects.filter(subject_identifier=self.subject_identifier):
                raise ValidationError, 'Attempt to insert duplicate value for' + \
                                       'subject_identifier {0} when saving {1}.'.format(self.subject_identifier,self)
        super(BaseSubject, self).save(*args, **kwargs)

    def __unicode__ (self):
        return "%s %s" % (self.subject_identifier, self.subject_type)
    
    class Meta:
        abstract=True
