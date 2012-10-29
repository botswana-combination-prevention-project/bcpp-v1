from django.db import models
from bhp_base_model.classes import BaseUuidModel


class DefaultValueLog(BaseUuidModel):

    subject_identifier = models.CharField(max_length=50)
    group_name = models.CharField(max_length=50)
    value_datetime = models.DateTimeField(null=True)
    error_message = models.TextField(max_length=500, null=True)
    objects = models.Manager()

    class Meta:
        app_label = 'bhp_lab_tracker'
