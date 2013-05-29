from django.db import models
from base_history_model import BaseHistoryModel


class HistoryModel(BaseHistoryModel):

    objects = models.Manager()

    class Meta:
        app_label = 'bhp_lab_tracker'
        #unique_together = (('subject_identifier', 'group_name', 'test_code', 'value_datetime'), ('source', 'source_identifier'), )
        unique_together = (('source', 'source_identifier', 'test_code', 'group_name', 'subject_identifier', 'value_datetime'), )
