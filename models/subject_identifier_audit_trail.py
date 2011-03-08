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



