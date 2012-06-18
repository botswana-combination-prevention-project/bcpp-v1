from django.db import models
from django.db.models import get_model
from django.utils.translation import ugettext_lazy as _
from django.core.validators import RegexValidator
from bhp_common.choices import YES_NO
from bhp_crypto.fields import EncryptedIdentityField
from bhp_base_model.validators import datetime_not_future, datetime_not_before_study_start
from bhp_variables.models import StudySite
from bhp_subject.classes import BaseSubject
from bhp_identifier.classes import Subject


class BaseConsent(BaseSubject):

    """ """
    
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
            
    may_store_samples = models.CharField(
        verbose_name = _("Sample storage"),
        max_length = 3, 
        choices = YES_NO, 
        help_text = _("Does the subject agree to have samples stored after the study has ended")
        )
    
    comment = models.CharField("Comment", 
        max_length=250, 
        blank=True
        )        

    def save(self, *args, **kwargs):
        
        RegisteredSubject = get_model('bhp_registration', 'RegisteredSubject')
        
        if not self.id:
            # allocate identifier, insert in registered subject
            subject = Subject()
            subject_identifier = subject.get_identifier(subject_type = self.get_subject_type(),
                                                    site = self.study_site.site_code,
                                                    registration_status = 'consented')
            
            #self.subject_identifier = RegisteredSubject.objects.register_subject(self, self.get_subject_type(), self.user_created)            
        else:
            # call registered_subject
            RegisteredSubject.objects.update_with(self)
            
        super(BaseConsent, self).save(*args, **kwargs)
    class Meta:
        abstract = True

