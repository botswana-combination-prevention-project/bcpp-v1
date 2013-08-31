from django.db import models
from base_history_model import BaseHistoryModel


class HistoryModel(BaseHistoryModel):

    objects = models.Manager()

    class Meta:
        app_label = 'bhp_lab_tracker'
        unique_together = (('source_model_name',
                            'source_app_label',
                            'source_identifier',
                            'test_code',
                            'group_name',
                            'subject_identifier',
                            'subject_type',
                            'value_datetime'), )
