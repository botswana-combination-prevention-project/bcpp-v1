from django.db import models
#from audit_trail.audit import AuditTrail
try:
    from bhp_sync.classes import BaseSyncModel as BaseUuidModel
except ImportError:
    from bhp_base_model.classes import BaseUuidModel
from lab_panel.models import Panel
from base_packing_list import BasePackingList


class BasePackingListItem(BaseUuidModel):

    requisition = models.CharField(
        max_length = 35,
        null = True,
        blank = False,
        help_text = "",
        )
    
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
    def packing_list_model(self):
        for field in self._meta.fields:
            try:
                if issubclass(field.rel.to, BasePackingList):
                    return (field.attname, field.rel.to)
            except:
                pass    
        return (None, None)   
    
    def view_packing_list(self):
        packing_list_field_attname, packing_list_model = self.packing_list_model()
        if packing_list_model:
            return '<a href="/admin/{app_label}/{object_name}/?q={pk}">{timestamp}</a>'.format(app_label = packing_list_model._meta.app_label,
                                                                                    object_name = packing_list_model._meta.object_name.lower(),
                                                                                    timestamp = packing_list_model.objects.get(pk=getattr(self, packing_list_field_attname)).timestamp,
                                                                                    pk = getattr(self, packing_list_field_attname),
                                                                                    )
        else:
            return 'packing list'
    view_packing_list.allow_tags = True

    
    def specimen(self):
        return '{item_reference}<BR>{requisition}</a>'.format(item_reference = self.item_reference,
                                                              requisition = self.requisition.replace('requisition', ''))
    specimen.allow_tags=True
       
    def get_subject_identifier(self):
        return ''
    
    class Meta:
        abstract = True
        #app_label = 'lab_packing'    
        ordering = ['created',]            
        
    
