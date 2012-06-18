from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.validators import RegexValidator
from bhp_crypto.fields import EncryptedLastnameField
from bhp_base_model.validators import datetime_not_future, datetime_not_before_study_start
from bhp_common.choices import YES_NO
from bhp_variables.models import StudySite
from bhp_identifier.classes import Subject
from bhp_subject.classes import BaseSubject


class BaseConsent(BaseSubject):

    """ """
        
    study_site = models.ForeignKey(StudySite,
        verbose_name = 'Site',
        help_text="This refers to the site or 'clinic area' where the subject is being consented."
        )
    
    consent_datetime = models.DateTimeField("Consent date and time",
        validators = [
            datetime_not_before_study_start,
            datetime_not_future,],
        )
        
    guardian_name = EncryptedLastnameField(
        verbose_name = _("Guardian\'s Last and first name (minors only)"),
        validators = [
            RegexValidator('^[A-Z]{1,50}\,[A-Z]{1,50}$', 'Invalid format. Format is \'LASTNAME, FIRSTNAME\'. All uppercase separated by a comma'),
            ],
        blank=True,
        null=True,    
        help_text = _('Required only if subject is a minor. Format is \'LASTNAME, FIRSTNAME\'. All uppercase separated by a comma'),
        )
            
    may_store_samples = models.CharField(
        verbose_name = _("Sample storage"),
        max_length = 3, 
        choices = YES_NO, 
        help_text = _("Does the subject agree to have samples stored after the study has ended")
        )
    
    comment = models.CharField("Comment", 
        max_length = 250, 
        blank=True
        )        

    def __unicode__(self):
        return unicode(self.subject_identifier)
    
    def save(self, *args, **kwargs):
        
        subject = Subject()
        if not self.id:
            # allocate new subject identifier
            self.subject_identifier = subject.get_identifier(self.get_subject_type(),
                                                             self.study_site.site_code)
        # create or update RegisteredSubject
        subject.update_register(self, 'subject_identifier', 
                                subject_identifier = subject.subject_identifier, 
                                registration_status = 'consented')
        super(BaseConsent, self).save(*args, **kwargs) 
 

    class Meta:
        abstract = True

    
