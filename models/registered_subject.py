from django.db import models
from base_subject import BaseSubject


class RegisteredSubjectManager(models.Manager):
    pass


class RegisteredSubject(BaseSubject):

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

    objects = RegisteredSubjectManager()
        
    def __unicode__ (self):
        return "%s %s (%s)" % (self.subject_identifier, self.subject_type, self.first_name)

    class Meta:
        app_label = 'bhp_registration'            

