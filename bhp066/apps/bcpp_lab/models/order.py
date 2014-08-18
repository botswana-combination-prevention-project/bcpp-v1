from datetime import datetime

from django.db import models

from edc.device.sync.models import BaseSyncUuidModel

from ..managers import OrderManager


class Order(BaseSyncUuidModel):

    order_datetime = models.DateTimeField(default=datetime.today())

    objects = OrderManager()

    def natural_key(self):
        return (self.order_datetime, )

    class Meta:
        app_label = 'bcpp_lab'
