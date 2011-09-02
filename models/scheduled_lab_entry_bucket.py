from datetime import datetime
from django.db import models
from django import forms
from django.core.urlresolvers import reverse
from bhp_common.models import MyBasicUuidModel
from bhp_appointment.models import Appointment
from bhp_entry.choices import ENTRY_STATUS
from bhp_entry.models import BaseEntryBucket
from bhp_lab_entry.managers import ScheduledLabEntryBucketManager
from lab_entry import LabEntry


class ScheduledLabEntryBucket(BaseEntryBucket):
    
    """Subject-specific list of required and scheduled lab as per normal visit schedule."""
    
    appointment = models.ForeignKey(Appointment, related_name='+')
    
    lab_entry = models.ForeignKey(LabEntry)
    
    objects = ScheduledLabEntryBucketManager()
    
    def get_absolute_url(self):
        return reverse('admin:bhp_entry_scheduledlabbucket_change', args=(self.id,))

    def __unicode__(self):        
        return '%s: %s' % (self.registered_subject.subject_identifier, self.lab_entry.panel.name)    

    
    class Meta:
        app_label = 'bhp_lab_entry'
        verbose_name = "Subject Scheduled Lab Bucket"
        ordering = ['registered_subject', 'lab_entry__panel__name','appointment',]
        unique_together = ['registered_subject', 'lab_entry', 'appointment',] 
