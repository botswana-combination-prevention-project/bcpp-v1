from datetime import datetime
from django.db import models
from django.core.urlresolvers import reverse
from bhp_registration.models import RegisteredSubject
from bhp_entry.choices import ENTRY_STATUS
from bhp_entry.models import BaseEntryBucket
from bhp_lab_entry.managers import AdditionalLabEntryBucketManager
from lab_entry import LabEntry 


class AdditionalLabEntryBucket(BaseEntryBucket):
    
    """List of required but unscheduled lab entries by registered_subject
    
    This model differs from ScheduledEntryBucket in that it is not attached to an
    appointment/visit_definition. 
    """
    
    lab_entry = models.ForeignKey(LabEntry)
        
    objects = AdditionalLabEntryBucketManager()

    def get_absolute_url(self):
        return reverse('admin:bhp_lab_entry_additionalentrybucket_change', args=(self.id,))

    def __unicode__(self):        
        return '%s: %s' % (self.registered_subject.subject_identifier, self.content_type_map)    
    
    class Meta:
        app_label = 'bhp_lab_entry'
        verbose_name = "Subject Additional Lab Entry Bucket"
        ordering = ['registered_subject', 'lab_entry__panel__name']

