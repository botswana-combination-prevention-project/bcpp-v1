from datetime import datetime

from django.core.urlresolvers import reverse
from django.db import models

from edc.audit.audit_trail import AuditTrail
from edc.device.sync.models import BaseSyncUuidModel

from apps.bcpp_subject.constants import NEW, CLOSED
from apps.bcpp_subject.models import SubjectVisit

from ..models import Aliquot, Panel
from django.core.exceptions import ValidationError

# from ..managers import PreOrderManager


class PreOrder(BaseSyncUuidModel):

    subject_visit = models.ForeignKey(SubjectVisit)

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
                # Can only link pre-order with existing aliquot record.
                Aliquot.objects.get(aliquot_identifier=self.aliquot_identifier)
            except Aliquot.DoesNotExist:
                raise ValidationError('Aliquot identifier "{}" does not exist'.format(self.aliquot_identifier))
            if self._meta.model.objects.filter(aliquot_identifier=self.aliquot_identifier).exclude(id=self.id).exists():
                # If i can get another preorder instance which is not me, then i know i am trying to re-use
                # an aliquot identifier, which is wrong. 
                # NOTE: Its being done this way instead of puttting unique=True in the aliquot_identifier field
                # definition because the field is nullable.
                raise ValidationError('You are attempting to re-use aliquout identifier "{}". This is not allowed.'.
                                      format(self.aliquot_identifier))
            else:
                # If i fail to get it, then proceed as normal.
                pass
            aliquot = Aliquot.objects.get(aliquot_identifier=self.aliquot_identifier)
            if aliquot.receive.registered_subject.subject_identifier != self.subject_visit.subject_identifier:
                raise ValidationError('The Aliquot you are attempting to use for "{}", belongs to "{}".'.
                                      format(self.subject_visit, aliquot.receive.registered_subject))
            self.status = CLOSED
        super(PreOrder, self).save(*args, **kwargs)

    def natural_key(self):
        return (self.order_identifier, )

    @property
    def model_url(self):
        app_label = 'bcpp_lab'
        model = 'preorder'
        if self.id:
            url = reverse('admin:{0}_{1}_change'.format(app_label, model), args=(self.id, ))
        else:
            url = reverse('admin:{0}_{1}_add'.format(app_label, model))
        return url

    class Meta:
        app_label = 'bcpp_lab'
        ordering = ['-preorder_datetime', ]
        unique_together = ('subject_visit', 'panel')
