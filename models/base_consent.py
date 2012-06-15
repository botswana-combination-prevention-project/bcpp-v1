from django.db import models
from django.db.models import get_model
from django.core.exceptions import ImproperlyConfigured
from django.utils.translation import ugettext_lazy as _
from bhp_base_model.fields import IdentityTypeField, IsDateEstimatedField
from bhp_base_model.validators import dob_not_future, dob_not_today, MinConsentAge, MaxConsentAge, GenderOfConsent
from bhp_common.choices import GENDER, YES_NO
from bhp_botswana.fields import EncryptedOmangField
from bhp_consent.models import BaseBaseConsentModel


class BaseConsentModel(BaseBaseConsentModel):
    
    """ because of the identity field, this is a BW model """

    dob = models.DateField(
        verbose_name = _("Date of birth"),
        validators = [
            dob_not_future, 
            dob_not_today,
            MinConsentAge,
            MaxConsentAge,            
            ],
        help_text=_("Format is YYYY-MM-DD"),
        )

    identity = EncryptedOmangField(
        verbose_name = _("Identity number (OMANG, etc)"), 
        max_length = 512, 
        unique = True,
        help_text = _("Use Omang, Passport number, driver's license number or Omang receipt number")
        )

    identity_type = IdentityTypeField()
    
    may_store_samples = models.CharField(
        verbose_name = _("Sample storage"),
        max_length = 3, 
        choices = YES_NO, 
        help_text = _("Does the subject agree to have samples stored after the study has ended")
        )

    gender = models.CharField(
        verbose_name = _("Gender"),
        max_length = 1, 
        choices = GENDER,
        validators = [
            GenderOfConsent,
            ]
        )
        
    is_dob_estimated = IsDateEstimatedField( 
        verbose_name = _("Is the subject's date of birth estimated?"),       
        )    

    def get_subject_type(self):
        raise ImproperlyConfigured('Method get_subject_type() must be overridden by the subclass to  \
                                    return the subject type (e.g. \'subject\', \'maternal\', \'infant\', ....')
    
    def save(self, *args, **kwargs):
        
        RegisteredSubject = get_model('bhp_registration', 'RegisteredSubject')
        
        if not self.id:
            # allocate identifier, insert in registered subject
            self.subject_identifier = RegisteredSubject.objects.register_subject(self, self.get_subject_type(), '')            
        else:
            # call registered_subject
            RegisteredSubject.objects.update_with(self)
            
        super(BaseConsentModel, self).save(*args, **kwargs) 
    
    
    class Meta:
        abstract = True

