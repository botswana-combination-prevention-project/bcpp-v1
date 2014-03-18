from datetime import datetime

from edc.device.device.classes import Device

from ..models import SubjectRequisitionInspector


class InspectorMixin(object):

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
                    device_id=device.device_id,
                    app_name=self._meta.app_label,
                    model_name=self._meta.object_name
                    )
