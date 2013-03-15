from django.db import models
try:
    from bhp_dispatch.models import BaseDispatchSyncUuidModel as BaseUuidModel
except ImportError:
    from bhp_base_model.models import BaseUuidModel


class BaseHistoryModel(BaseUuidModel):

    subject_identifier = models.CharField(max_length=25, db_index=True)
    report_datetime = models.DateTimeField(null=True, db_index=True)
    group_name = models.CharField(max_length=25)
    test_code = models.CharField(max_length=25)
    value = models.CharField(max_length=25)
    value_datetime = models.DateTimeField()
    source = models.CharField(max_length=50)
    source_identifier = models.CharField(max_length=50, null=True)
    history_datetime = models.DateTimeField(null=True)

    def include_for_dispatch(self):
        return True

    class Meta:
        abstract = True
