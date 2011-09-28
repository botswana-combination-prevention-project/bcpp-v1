from datetime import datetime
from django.db import models
from django.core.urlresolvers import reverse
from bhp_appointment.models import Appointment
from bhp_registration.models import RegisteredSubject
from bhp_entry.choices import ENTRY_STATUS
from bhp_entry.models import BaseEntryBucket
from bhp_lab_entry.managers import AdditionalLabEntryBucketManager
from lab_entry_unscheduled import LabEntryUnscheduled 


class AdditionalLabEntryBucket(BaseEntryBucket):
    
    """List of unscheduled lab entries by appointment
    
    Based on some condition, an additional lab may be added.
    an additional lab: 
    cannot be one that is scheduled for the current appointment
    cannot be an existing additional lab for this appointment
    """

    appointment = models.ForeignKey(Appointment, related_name='+')
    
    lab_entry_unscheduled = models.ForeignKey(LabEntryUnscheduled)
        
    objects = AdditionalLabEntryBucketManager()

    def get_absolute_url(self):
        return reverse('admin:bhp_lab_entry_additionallabentrybucket_change', args=(self.id,))

    def __unicode__(self):        
        return '%s: %s' % (self.registered_subject.subject_identifier, self.lab_entry_unscheduled)    
    
    class Meta:
        app_label = 'bhp_lab_entry'
        verbose_name = "Subject Additional Lab Entry Bucket"
        ordering = ['registered_subject', 'lab_entry_unscheduled__panel__name']
        unique_together = ['appointment', 'lab_entry_unscheduled',]

