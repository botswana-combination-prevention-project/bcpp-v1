from django.contrib import admin
from bhp_visit_tracking.classes import BaseVisitTrackingModelAdmin
from lab_panel.models import Panel
from lab_requisition.actions import flag_as_received, flag_as_not_received, flag_as_not_labelled
from lab_requisition.actions import print_requisition_label


class BaseRequisitionModelAdmin(BaseVisitTrackingModelAdmin):

    actions = [flag_as_received,
               flag_as_not_received,
               flag_as_not_labelled,
               print_requisition_label, ]

    def __init__(self, *args, **kwargs):
        super(BaseRequisitionModelAdmin, self).__init__(*args, **kwargs)
        self.fields = [
            self.visit_fieldname,
            "requisition_datetime",
            "is_drawn",
            "reason_not_drawn",
            "drawn_datetime",
            "site",
            "panel",
            "test_code",
            "aliquot_type",
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
            "site": admin.VERTICAL,
            }
        self.list_display = [
            'requisition_identifier',
            'specimen_identifier',
            'subject',
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
            "requisition_datetime",
            'is_receive_datetime',
            'is_labelled_datetime',
            'hostname_created', ]
        self.search_fields = [
            '{0}__appointment__registered_subject__subject_identifier'.format(self.visit_fieldname,),
            'specimen_identifier',
            'requisition_identifier']
        self.filter_horizontal = ["test_code", ]

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        panel_pk = request.GET.get('panel', 0)
        if db_field.name == 'panel':
            kwargs["queryset"] = Panel.objects.filter(pk=panel_pk)
        if db_field.name == 'aliquot_type':
            if Panel.objects.filter(pk=panel_pk):
                kwargs["queryset"] = Panel.objects.get(pk=panel_pk).aliquot_type.all()
        return super(BaseRequisitionModelAdmin, self).formfield_for_foreignkey(db_field,
                                                                               request,
                                                                               **kwargs)
