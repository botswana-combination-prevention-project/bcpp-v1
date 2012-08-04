from datetime import datetime
from django.db import models
from base_model import BaseModel


class DmisImportHistory(BaseModel):

    start_datetime = models.DateTimeField(default=datetime.today())
    end_datetime = models.DateTimeField(null=True)
    lock_name = models.CharField(max_length=50)
    objects = models.Manager()

    def __unicode__(self):
        return '%s on %s' % (self.start_datetime, self.end_datetime)

    class Meta:
        app_label = 'lab_import_dmis'
