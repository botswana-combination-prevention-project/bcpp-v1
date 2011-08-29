from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.validators import MinLengthValidator, MaxLengthValidator, RegexValidator
from bhp_common.validators import dob_not_future
from bhp_common.models import MyBasicUuidModel
from bhp_common.choices import GENDER, YES_NO, ART_STATUS_UNKNOWN, POS_NEG_UNKNOWN
from bhp_common.fields import InitialsField, IsDateEstimatedField
from bhp_lab_account.models import Account
from bhp_lab_patient.managers import PatientManager
from bhp_lab_patient.models import SimpleConsent
        
class Patient(MyBasicUuidModel):

    subject_identifier = models.CharField('Subject Identifier', 
        max_length=25, 
        unique=True, 
        help_text='', 
        db_index=True,
        )

    account = models.ManyToManyField(Account,
        null=True,
        blank=True,
        )

    initials = InitialsField()

    gender = models.CharField(
        verbose_name = _("Gender"),
        max_length=3, 
        choices=GENDER,
        )

    dob = models.DateField(
        verbose_name = _("Date of birth"),
        validators = [
            dob_not_future, 
            ],
        help_text=_("Format is YYYY-MM-DD"),
        )

    is_dob_estimated = IsDateEstimatedField( 
        verbose_name=_("Is the subject's date of birth estimated?"),       
    )    
    
    hiv_status = models.CharField(
        max_length = 10,
        choices = POS_NEG_UNKNOWN,
        default='UNKNOWN',
        ) 
    
    art_status = models.CharField(
        max_length = 10,
        choices = ART_STATUS_UNKNOWN,
        default='UNKNOWN',
        )

    simple_consent = models.ManyToManyField(SimpleConsent,
        verbose_name = _('Consent'),
        null=True,
        blank=True,
        )           

    comment = models.CharField("Comment", 
        max_length=250, 
        blank=True
        ) 

    objects = PatientManager()
               
    def get_absolute_url(self):
        return "/bhp_lab_patient/patient/%s/" % self.id   
    
    def __unicode__(self):
        return "%s" % (self.subject_identifier)
    
        
    class Meta:
        ordering = ["subject_identifier"]
        unique_together=['subject_identifier', ]
        app_label = 'bhp_lab_patient'  
        db_table = 'bhp_lab_registration_patient'              

