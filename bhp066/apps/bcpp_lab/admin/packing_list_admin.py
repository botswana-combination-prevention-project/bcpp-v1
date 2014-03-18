from django.contrib import admin

from edc.lab.lab_packing.admin import BasePackingListAdmin, BasePackingListItemAdmin

from ..forms import PackingListForm, PackingListItemForm
from ..models import PackingList, PackingListItem
from ..models import SubjectRequisition


class PackingListAdmin(BasePackingListAdmin):

    form = PackingListForm
    requisition = [SubjectRequisition, ]
    packing_list_item_model = PackingListItem

admin.site.register(PackingList, PackingListAdmin)


class PackingListItemAdmin(BasePackingListItemAdmin):

    form = PackingListItemForm
    requisition = [SubjectRequisition, ]

admin.site.register(PackingListItem, BasePackingListItemAdmin)
