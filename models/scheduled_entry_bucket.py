from datetime import datetime
from django.db import models
from django import forms
from django.core.urlresolvers import reverse
from bhp_common.models import MyBasicUuidModel
from bhp_appointment.models import Appointment
from bhp_entry.choices import ENTRY_STATUS
from bhp_entry.managers import ScheduledEntryBucketManager
from entry import Entry
from base_entry_bucket import BaseEntryBucket


class ScheduledEntryBucket(BaseEntryBucket):
    
    """Subject-specific list of required and scheduled entry as per normal visit schedule."""
    
    appointment = models.ForeignKey(Appointment, related_name='+')
    
    entry = models.ForeignKey(Entry)
    
    objects = ScheduledEntryBucketManager()
    
    def get_absolute_url(self):
        return reverse('admin:bhp_entry_scheduledentrybucket_change', args=(self.id,))

    def __unicode__(self):        
        return '%s: %s' % (self.registered_subject.subject_identifier, self.entry)    

    class Meta:
        app_label = 'bhp_entry'
        db_table = 'bhp_form_scheduledentrybucket'
        verbose_name = "Subject Scheduled Entry Bucket"
        ordering = ['registered_subject', 'entry','appointment',]
        unique_together = ['registered_subject', 'entry', 'appointment',] 
