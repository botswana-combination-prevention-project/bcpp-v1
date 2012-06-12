from django.db import models
#from audit_trail.audit import AuditTrail
try:
    from bhp_sync.classes import BaseSyncModel as BaseUuidModel
except ImportError:
    from bhp_base_model.classes import BaseUuidModel
from lab_panel.models import Panel


class BasePackingListItem(BaseUuidModel):

    item_reference = models.CharField(
        max_length = 25,
        )

    item_datetime = models.DateTimeField(
        null = True,
        blank = True,
        )    

    item_description = models.TextField(
        max_length = 100,
        null = True,
        blank = True,
        )    
    panel = models.ForeignKey(Panel,
        null = True,
        blank = True,
        )  
    
    #history = AuditTrail()    

    def get_subject_identifier(self):
        return ''
    
    class Meta:
        abstract = True
        #app_label = 'lab_packing'    
        ordering = ['created',]            
        
    
