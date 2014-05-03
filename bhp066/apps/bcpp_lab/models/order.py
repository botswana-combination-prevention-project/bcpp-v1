from datetime import datetime

from django.db import models

from edc.device.sync.models import BaseSyncUuidModel


class Order(BaseSyncUuidModel):

    order_datetime = models.DateTimeField(default=datetime.today())

    objects = models.Manager()

    class Meta:
        app_label = 'bcpp_lab'
