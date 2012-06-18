from django.db import models
from bhp_base_model.classes import BaseModel


class DerivedSubjectIdentifier(BaseModel):
    """Store subject identifiers derived from another participant, e.g. infant identifier from maternal identifier"""
    
    subject_identifier = models.CharField(
        max_length = 25,
        unique = True)
    
    base_identifier = models.CharField(
        max_length = 25)   
    
    def __unicode__(self):
        return self.subject_identifier
    
    class Meta:
        app_label = "bhp_identifier"
    
    