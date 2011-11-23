from django.contrib import admin
from django.utils.translation import ugettext as _
from bhp_common.models import MyModelAdmin, MyStackedInline
from bhp_netbook.models import Netbook, NetbookUser
from actions import netbook_uphosts


class NetbookAdmin (MyModelAdmin):

    list_display = ('name', 'db_name','make', 'model', 'ip_address', 'is_active', 'last_seen', 'serial_number')
    list_per_page = 25

    actions = [netbook_uphosts,]

admin.site.register(Netbook, NetbookAdmin)

class NetbookUserAdmin (MyModelAdmin):
    list_display = ('netbook','user', 'start_date', 'end_date')
    list_per_page = 25

admin.site.register(NetbookUser, NetbookUserAdmin)
