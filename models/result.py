from django.db import models
from lab_result.models import BaseResult
from order import Order


class Result(BaseResult):

    order = models.ForeignKey(Order)

    objects = models.Manager()

    def subject_identifier(self):
        return self.order.aliquot.receive.registered_subject

    def panel(self):
        return unicode(self.order.panel.edc_name)

    class Meta:
        app_label = 'lab_clinic_api'
        ordering = ['result_identifier']
