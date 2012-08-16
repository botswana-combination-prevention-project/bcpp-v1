from django.db import models
from django.core.urlresolvers import reverse

from lab_receive.models import BaseReceive
from bhp_registration.models import RegisteredSubject


class Receive(BaseReceive):
    """ Stores receiving information and is linked to :class:`bhp_registration.RegisteredSubject` for patient
    identification and demographics."""

    registered_subject = models.ForeignKey(RegisteredSubject, null=True)
    objects = models.Manager()

    def to_order(self):
        return '<a href="/admin/lab_clinic_api/order/?q={receive_identifier}">{receive_identifier}</a>'.format(receive_identifier=self.receive_identifier)
    to_order.allow_tags = True

    def get_absolute_url(self):
        return reverse('admin:lab_clinic_api_receive_change', args=(self.id,))

    def __unicode__(self):
        return '%s' % (self.receive_identifier)

    class Meta:
        app_label = 'lab_clinic_api'
