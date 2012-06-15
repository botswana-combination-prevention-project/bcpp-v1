from django.db import models
from django.db import IntegrityError
from django.utils.translation import ugettext_lazy as _
from django.core.validators import RegexValidator
from bhp_base_model.classes import BaseUuidModel
from bhp_common.choices import GENDER_UNDETERMINED
from bhp_base_model.fields import IsDateEstimatedField
from bhp_crypto.fields import EncryptedFirstnameField


class BaseSubject (BaseUuidModel):
       
    subject_consent_id = models.CharField(
        max_length=100, 
        null = True,
        blank = True,
        )
       
    # may be null so uniqueness is enforce in save() if not null
    subject_identifier = models.CharField(
        verbose_name = "Subject Identifier",
        max_length=36, 
        # unique = True,
        null = True, 
        blank = True,
        db_index=True,               
        )
    
    first_name = EncryptedFirstnameField(
        max_length=512,
        #validators = [RegexValidator(regex=r'$[A-Z]^', 
        #                             message='Ensure first name consists letters only in upper case, no spaces.'),]
        )
    
    initials = models.CharField(
        max_length=3,
        validators = [RegexValidator(regex=r'$[A-Z]^', 
                                    message='Ensure initials consist of letters only in upper case, no spaces.'),]
        )                    

    dob = models.DateField(
        verbose_name = _("Date of birth"),
        null=True,
        blank=True,
        help_text=_("Format is YYYY-MM-DD"),
        )

    is_dob_estimated = IsDateEstimatedField( 
        verbose_name=_("Is date of birth estimated?"),       
        null=True,
        blank=True,
        )    

    gender = models.CharField(
        verbose_name = "Gender",
        choices = GENDER_UNDETERMINED,
        max_length=1, 
        null = True,
        blank = True,
        )
        
    subject_type = models.CharField(
        max_length = 25,
        #choices=SUBJECT_TYPE,
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
                raise IntegrityError, 'Attempt to insert duplicate value for subject_identifier %s when saving %s.' % (self.subject_identifier,self,)
        super(BaseSubject, self).save(*args, **kwargs)

    def __unicode__ (self):
        return "%s %s" % (self.subject_identifier, self.subject_type)
    
    class Meta:
        abstract=True
