from django.contrib import admin
from edc.device.inspector.admin import BaseInspectorAdmin
from ..models import SubjectRequisitionInspector
from ..actions import set_inspectors_as_confirmed


class RequisitionInspectorAdmin(BaseInspectorAdmin):

    list_display = ['subject_identifier', 'requisition_datetime', 'is_confirmed', 'requisition_identifier', 'specimen_identifier', 'device_id']
    list_filter = ['subject_identifier', 'requisition_datetime', 'is_confirmed', 'requisition_identifier', 'specimen_identifier', 'device_id']
    search_fields = ['subject_identifier', 'requisition_datetime', 'is_confirmed', 'requisition_identifier', 'specimen_identifier', 'device_id']

    actions = [set_inspectors_as_confirmed]

admin.site.register(SubjectRequisitionInspector, RequisitionInspectorAdmin)
