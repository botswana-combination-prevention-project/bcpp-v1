from datetime import datetime
from django.db import models
from audit_trail.audit import AuditTrail
from bhp_sync.models import BaseSyncUuidModel


class BasePackingList(BaseSyncUuidModel):

    list_datetime = models.DateTimeField(
        default=datetime.today(),
        )

    list_comment = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        )

    list_items = models.TextField(
        max_length=1000,
        help_text='List specimen_identifier\'s. One per line.'
        )

    timestamp = models.CharField(
        max_length=35,
        null=True,
        )

    history = AuditTrail()

    def reference(self):
        return unicode(self.timestamp)

    def specimen_count(self):
        lst = filter(None, self.list_items.replace('\r', '').split('\n'))
        return len(lst)

    def view_list_items(self):
        return '<a href="/admin/{app_label}/{object_name}item/?q={pk}">{count} items</a>'.format(app_label=self._meta.app_label,
                                                                                                 object_name=self._meta.object_name.lower(),
                                                                                                 pk=self.id,
                                                                                                 count=self.specimen_count())
    view_list_items.allow_tags = True

    def __unicode__(self):
        return self.reference()

    def get_subject_identifier(self):
        return ''

    def save(self, *args, **kwargs):
        if not self.timestamp:
            self.timestamp = datetime.today().strftime('%Y%m%d%H%M%S%f')
        super(BasePackingList, self).save(*args, **kwargs)

    class Meta:
        abstract = True
        #app_label = 'lab_packing'
        ordering = ['list_datetime', ]
