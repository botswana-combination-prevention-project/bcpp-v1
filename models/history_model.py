from django.db import models
from bhp_base_model.classes import BaseUuidModel


class HistoryModel(BaseUuidModel):

    subject_identifier = models.CharField(max_length=25)
    group_name = models.CharField(max_length=25)
    test_code = models.CharField(max_length=25)
    value = models.CharField(max_length=25)
    value_datetime = models.DateTimeField()
    source = models.CharField(max_length=50)
    objects = models.Manager()

    class Meta:
        app_label = 'bhp_lab_tracker'
