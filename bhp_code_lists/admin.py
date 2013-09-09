from django.contrib import admin
from bhp_base_admin.admin import BaseModelAdmin
from models import DxCode, WcsDxAdult, WcsDxPed


class DxCodeAdmin(BaseModelAdmin):
    list_display = ('code', 'short_name')
    search_fields = ('code', 'short_name', 'long_name')
admin.site.register(DxCode, DxCodeAdmin)


class WcsDxAdultAdmin(BaseModelAdmin):
    list_display = ('code', 'short_name')
    search_fields = ('code', 'short_name', 'long_name')
admin.site.register(WcsDxAdult, WcsDxAdultAdmin)


class WcsDxPedAdmin(BaseModelAdmin):
    list_display = ('code', 'short_name')
    search_fields = ('code', 'short_name', 'long_name')
admin.site.register(WcsDxPed, WcsDxPedAdmin)
