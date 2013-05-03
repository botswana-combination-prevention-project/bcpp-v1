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
        blank=True)
    subject_identifier = models.CharField(
        max_length=25,
        null=True,
        editable=False,
        db_index=True,
        help_text="non-user helper field to simplify search and filtering")
    receive_identifier = models.CharField(
        max_length=25, editable=False, null=True, db_index=True,
        help_text="non-user helper field to simplify search and filter")
    objects = OrderManager()

    def protocol(self):
        return self.aliquot.receive.protocol

    def save(self, *args, **kwargs):
        self.subject_identifier = self.aliquot.receive.patient.subject_identifier
        self.receive_identifier = self.aliquot.receive_identifier
        super(Order, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return "/lab_order/order/%s/" % self.id

    def get_search_url(self):
        return "/laboratory/order/search/order/byword/%s/" % self.id

    class Meta:
        app_label = 'lab_order'
        db_table = 'bhp_lab_core_order'
