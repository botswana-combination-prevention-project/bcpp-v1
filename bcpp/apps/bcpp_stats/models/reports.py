from django.db import models

from edc_base.model.models import BaseModel


class Reports(BaseModel):

    title = models.CharField(max_length=150)

    description = models.TextField(max_length=250)

    class Meta:
        app_label = 'bcpp_stats'
