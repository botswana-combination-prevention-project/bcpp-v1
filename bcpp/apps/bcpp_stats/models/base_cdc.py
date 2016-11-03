from datetime import datetime

from django.db import models

from edc_base.model.models import BaseModel


class BaseCdc(BaseModel):

    _community = models.CharField(max_length=25)

    _title = models.CharField(max_length=150, null=True)

    _description = models.TextField(max_length=250, null=True)

    _filename = models.CharField(max_length=150)

    _import_datetime = models.DateTimeField(default=datetime.today())

    class Meta:
        abstract = True
