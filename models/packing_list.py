from datetime import datetime
from django.db import models
from bhp_common.models import MyBasicUuidModel


class PackingList(MyBasicUuidModel):

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

    def __unicode__(self):
        return self.pk

    class Meta:
        app_label = 'lab_packing'
        ordering = ['list_datetime',]


        
    
