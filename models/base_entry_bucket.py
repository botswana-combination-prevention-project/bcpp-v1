from django.db import models
from django.core.urlresolvers import reverse
from bhp_common.models import MyBasicUuidModel
from bhp_registration.models import RegisteredSubject
from bhp_entry.choices import ENTRY_STATUS

class BaseEntryBucket(MyBasicUuidModel):
    
    """Base model for list of required entries by registered_subject"""
    
    registered_subject = models.ForeignKey(RegisteredSubject, related_name='+')
    
    current_entry_title = models.CharField(
        max_length = 250,
        null = True,
        )
    entry_status = models.CharField(
        max_length = 25,
        choices = ENTRY_STATUS,
        default = 'NEW',        
        )

    due_datetime = models.DateTimeField()
    
    report_datetime = models.DateTimeField(
        null=True,
        blank=True,
        )    
    
    entry_comment = models.TextField(
        max_length = 250,
        null=True,
        blank=True,
        )
    
    close_datetime = models.DateTimeField(
        null = True,
        blank = True,
        )  
    
    fill_datetime = models.DateTimeField()
    

    def is_serialized(self):
        return super(BaseEntryBucket, self).is_serialized(True)
    
    class Meta:
        abstract = True
