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
from bhp_consent.models import BaseConsentModel

class ConsentModel(BaseConsentModel):

    subject_identifier = models.CharField('Subject Identifier', 
        max_length=25, 
        unique=True, 
        help_text='', 
        )

    def __unicode__(self):
        return unicode(self.subject_identifier)

    class Meta:
        #unique_together = (("first_name", "last_name", "dob"),)
        #ordering = ['-created']
        abstract = True
        
        
class ConsentNonUniqueModel(BaseConsentModel):

    subject_identifier = models.CharField('Subject Identifier', 
        max_length=25, 
        help_text='', 
        )

    def __unicode__(self):
        return unicode(self.subject_identifier)

    class Meta:
        #unique_together = (("first_name", "last_name", "dob"),)
        #ordering = ['-created']
        abstract = True        
