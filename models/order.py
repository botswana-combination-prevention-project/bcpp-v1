from django.db import models
from django.core.urlresolvers import reverse
from lab_order.models import BaseOrder
from aliquot import Aliquot
from panel import Panel


class Order(BaseOrder):
    """Stores orders and is in a one to many relation with :class:`Aliquot` where one aliquot may
    have multiple orders and in a one-to-many relation with :class:`Result` where one order
    should only have one final result (but not enforced by the DB)."""
    aliquot = models.ForeignKey(Aliquot)
    panel = models.ForeignKey(Panel)
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
        self.subject_identifier = self.aliquot.receive.registered_subject.subject_identifier
        self.receive_identifier = self.aliquot.receive_identifier
        super(Order, self).save(*args, **kwargs)

    def to_receive(self):
        return '<a href="/admin/lab_clinic_api/receive/?q={receive_identifier}">{receive_identifier}</a>'.format(receive_identifier=self.receive_identifier)
    to_receive.allow_tags = True

    def get_absolute_url(self):
        return reverse('admin:lab_clinic_api_order_change', args=(self.id,))

    def __unicode__(self):
        return '%s' % (self.order_identifier)

    class Meta:
        app_label = 'lab_clinic_api'
        ordering = ['order_identifier']
