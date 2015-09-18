from django.contrib import admin

from edc_base.modeladmin.admin import BaseModelAdmin

from ..models import GpsDevice


class GpsDeviceAdmin(BaseModelAdmin):
    instructions = []

admin.site.register(GpsDevice, GpsDeviceAdmin)
