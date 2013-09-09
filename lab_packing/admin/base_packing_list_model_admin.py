from bhp_base_admin.admin import BaseModelAdmin


class BasePackingListModelAdmin(BaseModelAdmin):

    fields = ('list_datetime', 'list_items', 'list_comment',)
    list_display = ('reference', 'view_list_items', 'list_datetime', 'list_comment',)
    list_filter = ('list_datetime',)
    search_fields = ('id', )
