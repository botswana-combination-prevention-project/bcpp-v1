from django.db import models
from bhp_base_model.classes import BaseUuidModel


class BaseHistoryModel(BaseUuidModel):

    subject_identifier = models.CharField(max_length=25)
    group_name = models.CharField(max_length=25)
    test_code = models.CharField(max_length=25)
    value = models.CharField(max_length=25)
    value_datetime = models.DateTimeField()
    source = models.CharField(max_length=50)
    source_identifier = models.CharField(max_length=50, null=True)
    history_datetime = models.DateTimeField(null=True)

    class Meta:
        abstract = True
