from django.db import models
from datetime import datetime
from django.conf import settings
from edc.audit.audit_trail import AuditTrail
from edc.lab.lab_requisition.models import BaseRequisition
from apps.bcpp_subject.models import SubjectVisit
from apps.bcpp_inspector.models import SubjectRequisitionInspector
from ..managers import SubjectRequisitionManager
from packing_list import PackingList


class SubjectRequisition(BaseRequisition):

    subject_visit = models.ForeignKey(SubjectVisit)

    packing_list = models.ForeignKey(PackingList, null=True, blank=True)

    subject_identifier = models.CharField(
        max_length=25,
        null=True,
        editable=False)

    history = AuditTrail()

    objects = SubjectRequisitionManager()

    def dispatch_container_lookup(self, using=None):
        return None

    def save_to_inspector(self, fields):
        SubjectRequisitionInspector.objects.create(
                subject_identifier=fields.get('subject_identifier'),
                requisition_datetime=datetime.strptime(str(fields.get('requisition_datetime')).split('T')[0], '%Y-%m-%d'),
                requisition_identifier=fields.get('requisition_identifier'),
                aliquot_type=fields.get('aliquot_type')[0],
                specimen_identifier=fields.get('specimen_identifier'),
                device_id=settings.DEVICE_ID,
                app_name='bcpp_lab',
                model_name='SubjectRequisition'
                )

    def natural_key(self):
        return (self.requisition_identifier,)

    def save(self, *args, **kwargs):
        self.subject_identifier = self.get_visit().get_subject_identifier()
        super(SubjectRequisition, self).save(*args, **kwargs)

    def get_visit(self):
        return self.subject_visit

    def get_subject_identifier(self):
        return self.get_visit().subject_identifier

    class Meta:
        app_label = 'bcpp_lab'
        verbose_name = 'Patient Lab Requisition'
