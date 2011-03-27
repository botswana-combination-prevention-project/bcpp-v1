from django.contrib import admin
from django.utils.translation import ugettext as _
from bhp_common.models import MyModelAdmin, MyStackedInline
from bhp_netbook.models import Netbook, NetbookUser

class NetbookAdmin (MyModelAdmin):
    list_display = ('name', 'make', 'model', 'serial_number')
    list_per_page = 25

admin.site.register(Netbook, NetbookAdmin)

class NetbookUserAdmin (MyModelAdmin):
    list_display = ('netbook','user', 'start_date', 'end_date')
    list_per_page = 25

admin.site.register(NetbookUser, NetbookUserAdmin)
