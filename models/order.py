from django.db import models
from lab_order.managers import OrderManager
from lab_aliquot.models import Aliquot
from lab_panel.models import Panel
from base_order import BaseOrder


class Order(BaseOrder):

    aliquot = models.ForeignKey(Aliquot)

    panel = models.ForeignKey(Panel)

    dmis_reference = models.IntegerField(
        null=True,
        blank=True,
        )

    objects = OrderManager()

    def get_absolute_url(self):
        return "/lab_order/order/%s/" % self.id

    def get_search_url(self):
        return "/laboratory/order/search/order/byword/%s/" % self.id

    class Meta:
        app_label = 'lab_order'
        db_table = 'bhp_lab_core_order'
