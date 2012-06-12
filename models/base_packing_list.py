from datetime import datetime
from django.db import models
from audit_trail.audit import AuditTrail
try:
    from bhp_sync.classes import BaseSyncModel as BaseUuidModel
except ImportError:
    from bhp_base_model.classes import BaseUuidModel


class BasePackingList(BaseUuidModel):

    list_datetime = models.DateTimeField(
        default = datetime.today(),
        )    

    list_comment = models.CharField(
        max_length = 100,
        null = True,
        blank = True,
        )
        
    list_items = models.TextField(
        max_length=1000,
        help_text = 'List specimen_identifier\'s. One per line.'
        )    

    history = AuditTrail()

    def __unicode__(self):
        return self.pk

    def get_subject_identifier(self):
        return ''

    class Meta:
        abstract = True
        #app_label = 'lab_packing'
        ordering = ['list_datetime',]


        
    
