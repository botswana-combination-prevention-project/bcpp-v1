from datetime import datetime
from django.db import models
from django.db.models import Count
from django.utils.translation import ugettext_lazy as _
from audit_trail.audit import AuditTrail
from base_subject import BaseSubject
from bhp_variables.models import StudySpecific, StudySite
from bhp_registration.managers import RegisteredSubjectManager
from bhp_common.fields import IsDateEstimatedField
from bhp_common.choices import YES_NO


class RegisteredSubject(BaseSubject):

    registration_identifier = models.CharField(
        max_length = 36,
        null=True,
        blank=True,
        #db_index=True,                       
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
    
    identity = models.CharField(
        max_length = 25,
        null=True,
        blank=True,
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
    
    may_store_samples = models.CharField(
        verbose_name = _("Sample storage"),
        max_length = 3, 
        choices = YES_NO,
        default = '?', 
        help_text = _("Does the subject agree to have samples stored after the study has ended")
        )

    
    comment = models.TextField(
        verbose_name = 'Comment',
        max_length = 250,
        null = True,
        blank = True,
        )
    
    objects = RegisteredSubjectManager()
    
    history = AuditTrail()            

    def is_serialized(self):
        return super(RegisteredSubject, self).is_serialized(True)
    
    def save(self, *args, **kwargs):
        # important: go to save() of super() FIRST to enforce unique subject_identifier
        super(RegisteredSubject, self).save(*args, **kwargs)
        # now you can add something below...
        
    def __unicode__ (self):
        if self.sid:
            return "%s %s (%s %s)" % (self.subject_identifier, self.subject_type, self.first_name, self.sid)
        else:
            return "%s %s (%s)" % (self.subject_identifier, self.subject_type, self.first_name)                    

    class Meta:
        app_label = 'bhp_registration'            

