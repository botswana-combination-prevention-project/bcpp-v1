from datetime import datetime

from django.db import models

from edc.audit.audit_trail import AuditTrail
from edc.device.device.classes import Device
from edc.lab.lab_requisition.models import BaseRequisition
from edc.map.classes import site_mappers

from apps.bcpp_inspector.models import SubjectRequisitionInspector
from apps.bcpp_subject.models import SubjectVisit

from ..managers import SubjectRequisitionManager

from .packing_list import PackingList


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

    def save_to_inspector(self, fields, instance_pk):
        if SubjectRequisitionInspector.objects.filter(subject_identifier=fields.get('subject_identifier'), requisition_identifier=fields.get('requisition_identifier')).count() == 0:
            device = Device()
            if (not fields.get('requisition_identifier')) or (fields.get('requisition_identifier') == ""):
                requisition_identifier = instance_pk
                specimen_identifier = instance_pk
            else:
                requisition_identifier = fields.get('requisition_identifier')
                specimen_identifier = fields.get('specimen_identifier')
            SubjectRequisitionInspector.objects.create(
                    subject_identifier=fields.get('subject_identifier'),
                    requisition_datetime=datetime.strptime(str(fields.get('requisition_datetime')).split('T')[0], '%Y-%m-%d'),  # FIXME: why strptime this??
                    requisition_identifier=requisition_identifier,
                    specimen_identifier=specimen_identifier,
                    device_id=device.get_device_id(),
                    app_name='bcpp_lab',
                    model_name='SubjectRequisition'
                    )

    def natural_key(self):
        return (self.requisition_identifier,)

    def save(self, *args, **kwargs):
        self.subject_identifier = self.get_visit().get_subject_identifier()
        super(SubjectRequisition, self).save(*args, **kwargs)

    def get_site_code(self):
        return site_mappers.get_current_mapper().map_code

    def get_visit(self):
        return self.subject_visit

    def get_subject_identifier(self):
        return self.get_visit().subject_identifier

    class Meta:
        app_label = 'bcpp_lab'
        verbose_name = 'Patient Lab Requisition'
