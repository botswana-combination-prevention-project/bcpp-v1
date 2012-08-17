from django.db import models
from lab_order.models import Order
from base_result import BaseResult


class Result(BaseResult):

    order = models.ForeignKey(Order)
    subject_identifier = models.CharField(
        max_length=25,
        null=True,
        editable=False,
        db_index=True,
        help_text="non-user helper field to simplify search and filtering")
    receive_identifier = models.CharField(
        max_length=25, editable=False, null=True, db_index=True,
        help_text="non-user helper field to simplify search and filter")
    objects = models.Manager()

    def save(self, *args, **kwargs):
        self.subject_identifier = self.order.aliquot.receive.patient.subject_identifier
        self.receive_identifier = self.order.aliquot.receive.receive_identifier
        if not self.result_identifier:
            self.result_identifier = self.get_identifier(self.order)
        super(Result, self).save(*args, **kwargs)

    def get_identifier(self, order):
        """ Prepares a result_identifier based on order_identifier. """
        cnt = self.__class__.objects.filter(order=order).count()
        cnt += 1
        return '{order_identifier}-{cnt}'.format(order_identifier=order.order_identifier, cnt=cnt.rjust(2, '0'))

    def get_absolute_url(self):
        return "/lab_result/result/%s/" % self.id

    def get_search_url(self):
        return "/laboratory/result/search/result/%s/" % self.result_identifier

    def get_document_url(self):
        return "/laboratory/result/document/%s/" % (self.result_identifier)

    class Meta:
        app_label = 'lab_result'
        db_table = 'bhp_lab_core_result'
        ordering = ['-result_identifier']
