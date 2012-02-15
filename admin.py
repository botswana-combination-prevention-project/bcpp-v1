from django.contrib import admin
from django.utils.translation import ugettext as _
from bhp_common.models import MyModelAdmin, MyStackedInline
from bhp_netbook.models import Netbook, NetbookUser, SvnHistory
from actions import netbook_uphosts #, netbook_update_svn


class NetbookAdmin (MyModelAdmin):

    list_display = ('name', 'is_active', 'db_name','make', 'model', 'ip_address', 'is_alive', 'last_seen', 'serial_number')
    list_per_page = 25
    list_filter = ('is_active', 'is_alive')

    actions = [netbook_uphosts,]

admin.site.register(Netbook, NetbookAdmin)

class NetbookUserAdmin (MyModelAdmin):
    list_display = ('netbook','user', 'start_date', 'end_date')
    list_per_page = 25

admin.site.register(NetbookUser, NetbookUserAdmin)


class SvnHistoryAdmin (MyModelAdmin):

    list_display = ('netbook','repo', 'last_revision_number', 'last_revision_date')
    list_filter = ('netbook','repo',)
    list_per_page = 50
    #actions = [netbook_update_svn,]

admin.site.register(SvnHistory, SvnHistoryAdmin)
