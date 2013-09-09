from django.db import models
from bhp_sync.models import BaseSyncUuidModel


class DefaultValueLog(BaseSyncUuidModel):

    subject_identifier = models.CharField(max_length=50)
    subject_type = models.CharField(max_length=25, null=True)
    group_name = models.CharField(max_length=50)
    value_datetime = models.DateTimeField(null=True)
    value = models.CharField(max_length=50, null=True, blank=True)
    error_message = models.TextField(max_length=500, null=True)
    objects = models.Manager()

    class Meta:
        app_label = 'bhp_lab_tracker'
