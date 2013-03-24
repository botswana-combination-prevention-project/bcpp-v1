from django.db import models
from django.core.urlresolvers import reverse
from bhp_appointment.models import Appointment
from bhp_entry.models import BaseEntryBucket
from bhp_lab_entry.managers import ScheduledLabEntryBucketManager
from lab_entry import LabEntry


class ScheduledLabEntryBucket(BaseEntryBucket):

    """Subject-specific list of required and scheduled lab as per normal visit schedule."""

    appointment = models.ForeignKey(Appointment, related_name='+')

    lab_entry = models.ForeignKey(LabEntry)

    objects = ScheduledLabEntryBucketManager()

    def natural_key(self):
        return self.lab_entry.natural_key() + self.appointment.natural_key()

    def deserialize_on_duplicate(self):
        return False

    def get_absolute_url(self):
        return reverse('admin:bhp_lab_entry_scheduledlabentrybucket_change', args=(self.id,))

    def __unicode__(self):
        return '%s: %s' % (self.registered_subject.subject_identifier, self.lab_entry.panel.name)

    class Meta:
        app_label = 'bhp_lab_entry'
        verbose_name = "Subject Scheduled Lab Bucket"
        ordering = ['registered_subject', 'lab_entry__panel__name', 'appointment', ]
        unique_together = ['registered_subject', 'lab_entry', 'appointment', ]
