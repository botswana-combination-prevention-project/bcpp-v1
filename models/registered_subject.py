from datetime import datetime
from django.db import models
from django.db.models import Count
from django.utils.translation import ugettext_lazy as _
from base_subject import BaseSubject
from bhp_variables.models import StudySpecific
from bhp_registration.managers import RegisteredSubjectManager
from bhp_common.fields import IsDateEstimatedField

class RegisteredSubject(BaseSubject):

    registration_identifier = models.CharField(
        max_length = 25,
        null=True,
        blank=True,
        )
        
    sid = models.CharField(
        verbose_name = "Randomization SID",
        max_length = 15,
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
    
    comment = models.TextField(
        verbose_name = 'Comment',
        max_length = 250,
        null = True,
        blank = True,
        )
    
    objects = RegisteredSubjectManager()
        
    def __unicode__ (self):
        return "%s %s (%s %s)" % (self.subject_identifier, self.subject_type, self.first_name, self.sid)

    class Meta:
        app_label = 'bhp_registration'            

