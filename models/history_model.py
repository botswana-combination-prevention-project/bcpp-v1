from django.db import models
from bhp_base_model.classes import BaseUuidModel


class HistoryModel(BaseUuidModel):

    subject_identifier = models.CharField(max_length=25)
    test_key = models.CharField(max_length=25)
    test_code = models.CharField(max_length=25)
    value = models.CharField(max_length=25)
    value_datetime = models.DateTimeField()
    objects = models.Manager()

    class Meta:
        app_label = 'lab_longitudinal'
