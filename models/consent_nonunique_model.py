from django.db import models
from bhp_consent.classes import BaseConsent

class ConsentNonUniqueModel(BaseConsent):

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
