from django.db import models
from django.utils.translation import ugettext_lazy as _
from audit_trail.audit import AuditTrail
from bhp_common.choices import YES_NO, POS_NEG_UNKNOWN, ALIVE_DEAD_UNKNOWN
from bhp_base_model.fields import IdentityTypeField
from bhp_variables.models import StudySite
from bhp_registration.managers import RegisteredSubjectManager
from bhp_crypto.classes import Crypter
from bhp_crypto.fields import EncryptedIdentityField, SaltField
from bhp_subject.classes import BaseSubject


class RegisteredSubject(BaseSubject):

    subject_consent_id = models.CharField(
        max_length=100, 
        null = True,
        blank = True,
        )
    
    registration_identifier = models.CharField(
        max_length = 36,
        null=True,
        blank=True,
        )
        
    sid = models.CharField(
        verbose_name = "SID",
        max_length = 15,
        null = True,
        blank = True,
        )

    study_site = models.ForeignKey(StudySite,
        verbose_name = 'Site',
        help_text="",
        null = True,
        blank = True,
        )
        
    relative_identifier = models.CharField(        
        verbose_name = "Identifier of immediate relation",
        max_length = 25,
        null = True,
        blank = True,
        help_text = "For example, mother's identifier, if available / appropriate"
        )
    
    identity = EncryptedIdentityField(
        unique = True,
        null=True,
        blank=True,
        )
    
    identity_type = IdentityTypeField()

    may_store_samples = models.CharField(
        verbose_name = _("Sample storage"),
        max_length = 3, 
        choices = YES_NO,
        default = '?', 
        help_text = _("Does the subject agree to have samples stored after the study has ended")
        )

    hiv_status = models.CharField(
        verbose_name = 'Hiv status',
        max_length = 15,
        choices = POS_NEG_UNKNOWN,
        null = True,
        )
    survival_status = models.CharField(
        verbose_name = 'Survival status',
        max_length = 15,
        choices = ALIVE_DEAD_UNKNOWN,
        null = True,
        )
    
    comment = models.TextField(
        verbose_name = 'Comment',
        max_length = 250,
        null = True,
        blank = True,
        )
    
    salt = SaltField(
        unique = True,
        )                        
    
    objects = RegisteredSubjectManager()
    
    history = AuditTrail()            
                                         
    def is_serialized(self):
        return super(RegisteredSubject, self).is_serialized(True)
            
    def __unicode__ (self):
        crypter = Crypter()
        if self.sid:
            return "{0} {1} ({2} {3})".format(self.subject_identifier, 
                                              self.subject_type, 
                                              crypter.mask_encrypted(self.first_name), 
                                              self.sid)
        else:
            return "{0} {1} ({2})".format(self.subject_identifier, 
                                          self.subject_type, 
                                          crypter.mask_encrypted(self.first_name))                    

    class Meta:
        app_label = 'bhp_registration' 
        verbose_name = 'Registered Subject'  
        ordering = ['subject_identifier',]   
        #unique_together = (('first_name', 'dob', 'initials'),)      

