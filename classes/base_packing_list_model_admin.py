from bhp_common.models import MyModelAdmin


class BasePackingListModelAdmin(MyModelAdmin):

    fields = ('list_datetime','list_items', 'list_comment',)
    
    list_display = ('pk', 'list_datetime', 'list_comment',)
    
    list_filter = ('list_datetime',)
    
    search_fields = ('id', )
