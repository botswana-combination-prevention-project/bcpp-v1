from datetime import datetime

from django.core.urlresolvers import reverse
from django.db import models

from edc.audit.audit_trail import AuditTrail
from edc.device.sync.models import BaseSyncUuidModel

from apps.bcpp_subject.constants import NEW, CLOSED

from ..models import Aliquot, Panel
from django.core.exceptions import ValidationError

# from ..managers import PreOrderManager


class PreOrder(BaseSyncUuidModel):

    subject_identifier = models.CharField(
        max_length=50,
        null=True,
        help_text="non-user helper field to simplify search and filtering"
    )

    panel = models.ForeignKey(
        Panel,
        null=True,
        blank=False,
    )

    aliquot_identifier = models.CharField(
        verbose_name='Aliquot Identifier',
        max_length=25,
        null=True,
        blank=False,
        help_text="Aliquot identifier"
    )

    preorder_datetime = models.DateTimeField(
        default=datetime.today()
    )

    status = models.CharField(
        max_length=50,
        default=NEW,
        null=True,
        help_text=""
    )

    history = AuditTrail()

    objects = models.Manager()

    def save(self, *args, **kwargs):
        if self.aliquot_identifier:
            try:
                Aliquot.objects.get(aliquot_identifier=self.aliquot_identifier)
            except Aliquot.DoesNotExist:
                raise ValidationError('Aliquot identifier "{}" does not exist'.format(self.aliquot_identifier))
            self.status = CLOSED
        super(PreOrder, self).save(*args, **kwargs)

    def natural_key(self):
        return (self.order_identifier, )

    @property
    def model_url(self):
        app_label = 'bcpp_lab'
        model = 'orderitem'
        if self.id:
            url = reverse('admin:{0}_{1}_change'.format(app_label, model), args=(self.id, ))
        else:
            url = reverse('admin:{0}_{1}_add'.format(app_label, model))
        return url

    @property
    def display_label(self):
        return self.panel.name

    @property
    def databrowse_url(self):
        return False

    @property
    def audit_trail_url(self):
        return False

    class Meta:
        app_label = 'bcpp_lab'
        ordering = ['-preorder_datetime', ]
