from django.db import models
from bhp_base_model.classes import BaseModel


class SubjectIdentifier(BaseModel):
    """Store subject identifiers as allocated and use the pk as a unique sequence for the new subject identifier.
    
    Will not include identifiers derived from those of existing subject. For example infant and partner subject
    identifiers are not included in this model."""
    
    subject_identifier = models.CharField(max_length = 25, unique=True)
    
    seed = models.IntegerField()
    
    @property
    def sequence(self):
        """return a padded sequence segment of the subject identifier based on the auto-increment integer primary key"""
        if not self.seed:
            raise TypeError('Seed cannot be None.')
        return str(self.pk).rjust(len(self.seed),'0')    
    
    def __unicode__(self):
        return self.subject_identifier
    
    
    class Meta:
        app_label = "bhp_identifier"
    
    
