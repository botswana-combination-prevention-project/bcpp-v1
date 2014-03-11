from datetime import datetime

from django.db import models

from edc.device.device.classes import Device
from edc.lab.lab_requisition.models import BaseRequisition
from edc.map.classes import site_mappers

from apps.bcpp.choices import COMMUNITIES
from apps.bcpp_inspector.models import SubjectRequisitionInspector

from .packing_list import PackingList


class BaseSubjectRequisition(BaseRequisition):

    packing_list = models.ForeignKey(PackingList, null=True, blank=True)

    subject_identifier = models.CharField(
        max_length=25,
        null=True,
        editable=False)

    community = models.CharField(max_length=25, choices=COMMUNITIES, null=True, editable=False)

    def save(self, *args, **kwargs):
        super(BaseSubjectRequisition, self).save(*args, **kwargs)

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

    def get_site_code(self):
        return site_mappers.get_current_mapper().map_code

    def get_visit(self):
        raise TypeError('method \'subject_visit()\' in BaseSubjectRequisition must be overidden by the subclass')

    def get_subject_identifier(self):
        return self.get_visit().subject_identifier

    def dashboard(self):
        raise TypeError('method \'dashboard()\' in BaseSubjectRequisition must be overidden by the subclass')

    class Meta:
        abstract = True
