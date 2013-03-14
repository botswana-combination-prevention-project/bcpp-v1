from django.db import models
from bhp_base_model.models import BaseUuidModel
from bhp_dispatch.models import BaseDispatchSyncUuidModel

class BaseHistoryModel(BaseDispatchSyncUuidModel):

    subject_identifier = models.CharField(max_length=25, db_index=True)
    report_datetime = models.DateTimeField(null=True, db_index=True)
    group_name = models.CharField(max_length=25)
    test_code = models.CharField(max_length=25)
    value = models.CharField(max_length=25)
    value_datetime = models.DateTimeField()
    source = models.CharField(max_length=50)
    source_identifier = models.CharField(max_length=50, null=True)
    history_datetime = models.DateTimeField(null=True)

    class Meta:
        abstract = True
