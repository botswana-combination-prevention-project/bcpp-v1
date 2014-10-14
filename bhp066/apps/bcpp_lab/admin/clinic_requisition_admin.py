from django.contrib import admin

from ..classes import ClinicRequisitionModelAdmin
from ..models import ClinicRequisition
from ..forms import ClinicRequisitionForm


class ClinicRequisitionAdmin(ClinicRequisitionModelAdmin):

    form = ClinicRequisitionForm

    def __init__(self, *args, **kwargs):
        super(ClinicRequisitionAdmin, self).__init__(*args, **kwargs)
        self.fields = [
            self.visit_fieldname,
            "requisition_datetime",
            "is_drawn",
            "reason_not_drawn",
            "drawn_datetime",
            "panel",
            "test_code",
            "aliquot_type",
            "site",
            "item_type",
            "item_count_total",
            "estimated_volume",
            "priority",
            "comments", ]
        self.radio_fields = {
            "is_drawn": admin.VERTICAL,
            "reason_not_drawn": admin.VERTICAL,
            "item_type": admin.VERTICAL,
            "priority": admin.VERTICAL,
            }
        self.list_display = [
            'requisition_identifier',
            'specimen_identifier',
            'subject',
            'dashboard',
            'aliquot',
            'visit',
            "requisition_datetime",
            "panel",
            'hostname_created',
            "priority",
            'is_receive',
            'is_labelled',
            'is_packed',
            'is_lis',
            'is_receive_datetime',
            'is_labelled_datetime', ]
        self.list_filter = [
            "priority",
            'is_receive',
            'is_labelled',
            'is_packed',
            'is_lis',
            'community',
            "requisition_datetime",
            'is_receive_datetime',
            'is_labelled_datetime',
            'hostname_created', ]
        self.search_fields = [
            '{0}__appointment__registered_subject__subject_identifier'.format(self.visit_fieldname,),
            'specimen_identifier',
            'requisition_identifier',
             'panel__name'
            ]
        self.filter_horizontal = ["test_code", ]

admin.site.register(ClinicRequisition, ClinicRequisitionAdmin)
