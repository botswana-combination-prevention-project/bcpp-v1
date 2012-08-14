from django.db import models
from django.core.urlresolvers import reverse
from lab_order.models import BaseOrder
from aliquot import Aliquot
from panel import Panel


class Order(BaseOrder):

    aliquot = models.ForeignKey(Aliquot)

    panel = models.ForeignKey(Panel)

    import_datetime = models.DateTimeField(null=True)

    objects = models.Manager()

    def get_absolute_url(self):
        return reverse('admin:lab_clinic_api_order_change', args=(self.id,))

    def subject_identifier(self):
        if self.aliquot.receive.registered_subject is not None:
            return self.aliquot.receive.registered_subject.subject_identifier
        else:
            return 'unknown'

    def __unicode__(self):
        return '%s' % (self.order_identifier)

    class Meta:
        app_label = 'lab_clinic_api'
        ordering = ['order_identifier']
