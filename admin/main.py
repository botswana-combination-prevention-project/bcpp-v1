from django.contrib import admin
from bhp_base_admin.admin import BaseModelAdmin
from bhp_netbook.models import Netbook, NetbookUser
from bhp_netbook.actions import netbook_uphosts 


class NetbookAdmin (BaseModelAdmin):
    list_display = (
        'name',
        'is_active',
        'db_name',
        'make',
        'model',
        'ip_address',
        'is_alive',
        'last_seen',
        'serial_number'
        )
    list_per_page = 25
    list_filter = ('is_active', 'is_alive')

    actions = [netbook_uphosts,]

admin.site.register(Netbook, NetbookAdmin)

class NetbookUserAdmin (BaseModelAdmin):
    list_display = ('netbook','user', 'start_date', 'end_date')
    list_per_page = 25

admin.site.register(NetbookUser, NetbookUserAdmin)

