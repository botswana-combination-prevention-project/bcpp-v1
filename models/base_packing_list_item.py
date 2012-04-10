from django.db import models
#from audit_trail.audit import AuditTrail
from bhp_common.models import MyBasicUuidModel
from lab_panel.models import Panel


class BasePackingListItem(MyBasicUuidModel):

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
        
    
