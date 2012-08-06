from django.db import models
from lab_order.models import Order
from base_result import BaseResult


class Result(BaseResult):

    order = models.ForeignKey(Order)

    objects = models.Manager()

    def __unicode__(self):
        return '%s' % (self.result_identifier)

    def get_absolute_url(self):
        return "/lab_result/result/%s/" % self.id

    def get_search_url(self):
        return "/laboratory/result/search/result/%s/" % self.result_identifier

    def get_document_url(self):
        return "/laboratory/result/document/%s/" % (self.result_identifier)

    class Meta:
        app_label = 'lab_result'
        db_table = 'bhp_lab_core_result'
        ordering = ['result_identifier', 'order', 'result_datetime']
