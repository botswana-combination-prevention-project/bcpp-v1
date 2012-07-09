from datetime import date
from django.db import models
from bhp_base_model.fields import MyUUIDField
from bhp_base_model.classes import BaseModel


class SubjectIdentifierAuditTrail(BaseModel):
    """
    A table to track every attempt to allocate a subject identifier
    to a subject 'by this device'. If a subject's record is deleted
    the record in this table remains. So this is not a master list of
    valid identifiers. 
    
    See also AllocateSubjectIdentifier()
    
    """
    subject_consent_id = MyUUIDField()
    
    subject_identifier = models.CharField(
        max_length=25,
        unique=True
        )
    
    #    first_name = models.CharField(max_length=250) 
    #    
    #    initials = models.CharField(max_length=3)
    #    
    #    dob = DobField(
    #        null=True
    #        )
    
    date_allocated = models.DateTimeField(
        default=date.today()
        )
    
    def __unicode__(self):
        #return '%s %s' % (self.subject_identifier, self.initials)
        return '%s' % (self.subject_identifier)
        
    class Meta:
        ordering = ['-date_allocated']
        app_label = 'bhp_registration'
