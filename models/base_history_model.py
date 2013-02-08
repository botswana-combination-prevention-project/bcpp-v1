from django.db import models
from bhp_sync.models import BaseSyncUuidModel


class BaseHistoryModel(BaseSyncUuidModel):

    subject_identifier = models.CharField(max_length=25)
    report_datetime = models.DateTimeField(null=True)
    group_name = models.CharField(max_length=25)
    test_code = models.CharField(max_length=25)
    value = models.CharField(max_length=25)
    value_datetime = models.DateTimeField()
    source = models.CharField(max_length=50)
    source_identifier = models.CharField(max_length=50, null=True)
    history_datetime = models.DateTimeField(null=True)

    class Meta:
        abstract = True
