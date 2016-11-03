from django.db import models

from edc_base.model.models import BaseModel


class Report01(BaseModel):

    index = models.IntegerField()

    label = models.CharField(max_length=25)

    value = models.CharField()

    value_format = models.CharField()

    class Meta:
        app_label = 'bcpp_reports'
