from django.contrib import admin
from edc.lab.lab_packing.admin import BasePackingListAdmin, BasePackingListItemAdmin
from ..classes import SubjectRequisitionModelAdmin
from ..models import SubjectRequisition
from ..models import PackingList, PackingListItem
from ..forms import SubjectRequisitionForm, PackingListForm, PackingListItemForm


class SubjectRequisitionAdmin(SubjectRequisitionModelAdmin):

    form = SubjectRequisitionForm

    def __init__(self, *args, **kwargs):
        super(SubjectRequisitionAdmin, self).__init__(*args, **kwargs)
        self.fields = [
            self.visit_fieldname,
            "requisition_datetime",
            "is_drawn",
            "reason_not_drawn",
            "drawn_datetime",
            "panel",
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
            }
        self.list_display = [
            'requisition_identifier',
            'specimen_identifier',
            'subject',
            'dashboard',
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
            'panel__name']

admin.site.register(SubjectRequisition, SubjectRequisitionAdmin)


class PackingListAdmin(BasePackingListAdmin):

    form = PackingListForm
    requisition = [SubjectRequisition, ]
    packing_list_item_model = PackingListItem

admin.site.register(PackingList, PackingListAdmin)


class PackingListItemAdmin(BasePackingListItemAdmin):

    form = PackingListItemForm
    requisition = [SubjectRequisition, ]

admin.site.register(PackingListItem, BasePackingListItemAdmin)
