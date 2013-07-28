from django.db import models
from django.core.urlresolvers import reverse
from bhp_content_type_map.models import ContentTypeMap
from bhp_entry.models import BaseEntryBucket
from bhp_entry.managers import AdditionalEntryBucketManager


class AdditionalEntryBucket(BaseEntryBucket):

    """List of required but unscheduled entries by registered_subject such as off-study, death, adverse event, etc (not attached to appointment model).

    This model differs from ScheduledEntryBucket in that it is not attached to an
    appointment/visit_definition. Also, it is not attached to the Entry model and instead refers
    directly to the ContentType model.
    """
    rule_name = models.CharField(
        max_length=50,
        null=True,
        help_text='Name of rule that created the entry',
        db_index=True)

    content_type_map = models.ForeignKey(ContentTypeMap,
            related_name='+',
            verbose_name='entry form / model')

    objects = AdditionalEntryBucketManager()
    #objects = models.Manager()

    def get_absolute_url(self):
        return reverse('admin:bhp_entry_additionalentrybucket_change', args=(self.id,))

    def __unicode__(self):
        return '{0}: {1}' % (self.registered_subject.subject_identifier, self.content_type_map)

    def is_keyed(self):
        """ Confirm if model instance exists / is_keyed. """
        model = models.get_model(
                        self.content_type_map.content_type.app_label,
                        self.content_type_map.content_type.model)

        if model.objects.filter(registered_subject=self.registered_subject):
            is_keyed = True
        else:
            is_keyed = False
        return is_keyed

    class Meta:
        app_label = 'bhp_entry'
        verbose_name = "Subject Additional Entry Bucket"
        ordering = ['registered_subject', 'content_type_map', ]
        unique_together = ['registered_subject', 'content_type_map', ]
