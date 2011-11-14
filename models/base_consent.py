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
from bhp_consent.models import BaseBaseConsentModel

class BaseConsentModel(BaseBaseConsentModel):

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

    identity = models.CharField(
        verbose_name=_("Identity number (OMANG, etc)"), 
        max_length=25, 
        unique=True,
        help_text=_("Use Omang, Passport number, driver's license number or Omang receipt number")
        )

    identity_type = IdentityTypeField()
    
    may_store_samples = models.CharField(
        verbose_name = _("Sample storage"),
        max_length=3, 
        choices=YES_NO, 
        help_text=_("Does the subject agree to have samples stored after the study has ended")
        )

    gender = models.CharField(
        verbose_name = _("Gender"),
        max_length=1, 
        choices=GENDER,
        validators=[
            GenderOfConsent,
            ]
        )
        
    is_dob_estimated = IsDateEstimatedField( 
        verbose_name=_("Is the subject's date of birth estimated?"),       
        )    



    class Meta:
       abstract = True

