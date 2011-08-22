from datetime import datetime
from django.db import models
from django.core.urlresolvers import reverse
from bhp_common.models import ContentTypeMap
from bhp_registration.models import RegisteredSubject
from bhp_entry.choices import ENTRY_STATUS
from bhp_entry.models import BaseEntryBucket 
from bhp_entry.managers import AdditionalEntryBucketManager

class AdditionalEntryBucket(BaseEntryBucket):
    
    """List of required but unscheduled entries by registered_subject such as off-study, death, adverse event, etc. (not attached to appointment model)
    
    This model differs from ScheduledEntryBucket in that it is not attached to an
    appointment. Also, it is not attached to the Entry model and instead refers 
    directly to the ContentType model.
    """
    
    content_type_map = models.ForeignKey(ContentTypeMap,
            related_name='+',
            verbose_name = 'entry form / model')
    
    objects = AdditionalEntryBucketManager()

    def get_absolute_url(self):
        return reverse('admin:bhp_entry_additionalentrybucket_change', args=(self.id,))

    def __unicode__(self):        
        return '%s: %s' % (self.registered_subject.subject_identifier, self.content_type_map)    
    
    class Meta:
        app_label = 'bhp_entry'
        db_table = 'bhp_form_additionalentrybucket'
        verbose_name = "Subject Additional Entry Bucket"
        ordering = ['registered_subject', 'content_type_map',]
        unique_together = ['registered_subject', 'content_type_map', ] 
