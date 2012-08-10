from django.db import models
from lab_order.models import BaseOrder
from aliquot import Aliquot
from panel import Panel


class Order(BaseOrder):

    aliquot = models.ForeignKey(Aliquot)

    panel = models.ForeignKey(Panel)

    objects = models.Manager()

    def subject_identifier(self):
        if self.aliquot.receive.registered_subject is not None:
            return self.aliquot.receive.registered_subject.subject_identifier
        else:
            return 'unknown'

    def __unicode__(self):
        return '%s' % (self.order_identifier)

    class Meta:
        app_label = 'lab_clinic_api'
        #ordering =['result_identifier']
