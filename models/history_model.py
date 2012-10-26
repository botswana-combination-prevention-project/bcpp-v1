from django.db import models
from base_history_model import BaseHistoryModel


class HistoryModel(BaseHistoryModel):

    objects = models.Manager()

    class Meta:
        app_label = 'bhp_lab_tracker'
