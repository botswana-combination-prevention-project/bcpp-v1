from datetime import datetime

from django.db import models

from edc.device.device.classes import Device

from ..models import SubjectRequisitionInspector


class InspectorMixin(models.Model):

    def save_to_inspector(self, fields, instance_pk, using):
        if SubjectRequisitionInspector.objects.using(using).filter(subject_identifier=fields.get('subject_identifier'), requisition_identifier=fields.get('requisition_identifier')).count() == 0:
            device = Device()
            if (not fields.get('requisition_identifier')) or (fields.get('requisition_identifier') == ""):
                requisition_identifier = instance_pk
                specimen_identifier = instance_pk
            else:
                requisition_identifier = fields.get('requisition_identifier')
                specimen_identifier = fields.get('specimen_identifier')
            SubjectRequisitionInspector.objects.using(using).create(
                subject_identifier=fields.get('subject_identifier'),
                requisition_datetime=datetime.strptime(str(fields.get('requisition_datetime')), '%Y-%m-%dT%H:%M:%S'),
                requisition_identifier=requisition_identifier,
                specimen_identifier=specimen_identifier,
                device_id=device.device_id,
                app_name=self._meta.app_label,
                model_name=self._meta.object_name
            )

    class Meta:
        abstract = True
