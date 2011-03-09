from django.db import models
from django.utils.translation import ugettext_lazy as _
from bhp_common.fields import MyUUIDField
from bhp_common.models import MyBasicUuidModel


class SubjectIdentifierAuditTrail(MyBasicUuidModel):
    """
    A table to track every attempt to allocate a subject identifier
    to a consented subject 'by this device'. If a subject consent is deleted
    the record in this table remains. So this is not a master list of
    valid identifiers. 
    See also AllocateSubjectIdentifier()
    """
    subject_consent_id = MyUUIDField()
    subject_identifier = models.CharField(max_length=25)
    first_name = models.CharField(max_length=250) 
    initials = models.CharField(max_length=3)
    date_allocated = models.DateTimeField()
    
    def __unicode__(self):
        return self.subject_identifier
        
    class Meta:
        ordering = ['-date_allocated']
        app_label = 'bhp_registration'
