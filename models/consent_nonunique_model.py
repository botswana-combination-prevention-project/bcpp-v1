from django.db import models
from django.utils.translation import ugettext_lazy as _
from bhp_consent.models import BaseConsentModel

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
