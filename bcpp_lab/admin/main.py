from django.contrib import admin
from lab_packing.admin import BasePackingListAdmin, BasePackingListItemAdmin
from bcpp_lab.classes import SubjectRequisitionModelAdmin
from bcpp_lab.models import SubjectRequisition
from bcpp_lab.models import PackingList, PackingListItem
from bcpp_lab.forms import SubjectRequisitionForm, PackingListForm, PackingListItemForm


class SubjectRequisitionAdmin(SubjectRequisitionModelAdmin):

    form = SubjectRequisitionForm

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
