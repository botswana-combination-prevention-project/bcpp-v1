from django.db import models
from bhp_base_model.models import BaseModel


TRACK_STATUS = (('IN', 'In'), ('OUT', 'Out'))


class MobileDataTracker(BaseModel):

    app_label = models.CharField(max_length=35)

    model_name = models.CharField(max_length=35)

    identifier = models.CharField(max_length=36)

    track_datetime = models.DateTimeField()

    track_status = models.CharField(max_length=15, choices=TRACK_STATUS)

    objects = models.Manager()

    def __unicode__(self):
        return "%s %s" % (self.model_name, self.identifier)

    class Meta:
        unique_together = ['app_label', 'model_name', 'identifier']
        app_label = 'bhp_netbook'
