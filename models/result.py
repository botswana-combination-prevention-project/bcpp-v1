from django.db import models
from lab_result.models import BaseResult
from order import Order


class Result(BaseResult):

    order = models.ForeignKey(Order)

    import_datetime = models.DateTimeField(null=True)

    objects = models.Manager()

    def subject_identifier(self):
        return self.order.aliquot.receive.registered_subject

    def panel(self):
        return unicode(self.order.panel.edc_name)

    def received(self):
        return '<a href="{0}">{1}</a>'.format(self.order.aliquot.receive.get_absolute_url(), self.order.aliquot.receive)
    received.allow_tags = True

    def ordered(self):
        return '<a href="{0}">{1}</a>'.format(self.order.get_absolute_url(), self.order)
    ordered.allow_tags = True

    class Meta:
        app_label = 'lab_clinic_api'
        ordering = ['result_identifier']
