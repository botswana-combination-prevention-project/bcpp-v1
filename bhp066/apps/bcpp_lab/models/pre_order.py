from datetime import datetime

from django.core.urlresolvers import reverse
from django.db import models
from django.core.exceptions import ValidationError, ObjectDoesNotExist

from edc.device.sync.models import BaseSyncUuidModel
from edc_base.audit_trail import AuditTrail
from edc_constants.constants import NEW, PENDING

from bhp066.apps.bcpp_subject.constants import POC_VIRAL_LOAD
from bhp066.apps.bcpp_subject.models import SubjectVisit

from ..models import Aliquot, Panel
from ..managers import PreOrderManager


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

    objects = PreOrderManager()

    history = AuditTrail()

    def save(self, *args, **kwargs):
        if not self.aliquot_identifier:
            self.status = NEW
        else:
            try:
                Aliquot.objects.get(
                    aliquot_identifier=self.aliquot_identifier,
                    receive__registered_subject__subject_identifier=self.subject_visit.subject_identifier)
            except Aliquot.DoesNotExist:
                raise ValidationError(
                    'Aliquot identifier "{}" does not exist for this subject'.format(self.aliquot_identifier))
            try:
                self.__class__.objects.get(
                    aliquot_identifier=self.aliquot_identifier).exclude(id=self.id)
            except ObjectDoesNotExist:
                raise ValidationError(
                    'You are attempting to re-use aliquot identifier "{}". This is not allowed.'.format(
                        self.aliquot_identifier))
            if 'status' not in kwargs.get('update_fields', []):
                self.status = PENDING
        super(PreOrder, self).save(*args, **kwargs)

    def natural_key(self):
        return self.subject_visit.natural_key() + self.panel.natural_key()

    def __unicode__(self):
        return str((self.subject_visit, self.panel))

    @property
    def model_url(self):
        app_label = 'bcpp_lab'
        model = 'preorder'
        if self.id:
            url = reverse('admin:{0}_{1}_change'.format(app_label, model), args=(self.id, ))
        else:
            url = reverse('admin:{0}_{1}_add'.format(app_label, model))
        return url

    def result(self):
        url = reverse('admin:bcpp_subject_pimavl_add')
        if self.panel.name == POC_VIRAL_LOAD and self.aliquot_identifier:
            return '<a href="{0}?subject_visit={1}">result</a>'.format(url, self.subject_visit.id)
        else:
            return None
    result.allow_tags = True

    class Meta:
        app_label = 'bcpp_lab'
        ordering = ['-preorder_datetime', ]
        unique_together = (('subject_visit', 'panel'),)
