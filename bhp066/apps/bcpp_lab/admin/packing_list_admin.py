from django.contrib import admin

from edc.lab.lab_packing.admin import BasePackingListAdmin, BasePackingListItemAdmin
from edc.map.classes import site_mappers

from ..forms import PackingListForm, PackingListItemForm
from ..models import PackingList, PackingListItem


class PackingListAdmin(BasePackingListAdmin):

    form = PackingListForm

    fields = ('destination', 'list_items', 'community', 'list_comment',)
    list_display = ('reference', 'view_list_items', 'list_datetime',
                    'list_comment', 'destination', 'received', )
    list_filter = ('list_datetime', 'destination', 'received', 'community', 'list_comment')
    search_fields = ('id', 'list_comment')

    def get_form_post(self, form, request, obj=None, **kwargs):
            form = super(PackingListAdmin, self).get_form_post(form, request, obj, **kwargs)
            form.base_fields['community'].initial = site_mappers.get_current_mapper().map_area
            return form

admin.site.register(PackingList, PackingListAdmin)


class PackingListItemAdmin(BasePackingListItemAdmin):

    form = PackingListItemForm

    search_fields = ('packing_list__pk', 'packing_list__timestamp', 'item_description', 'item_reference', )
    list_display = ('specimen', 'priority', 'panel', 'description', 'gender',
                    'drawn_datetime', 'clinician', 'view_packing_list', 'received', 'received_datetime',)
    list_filter = ('created', 'panel', 'received', 'received_datetime',)


admin.site.register(PackingListItem, BasePackingListItemAdmin)
