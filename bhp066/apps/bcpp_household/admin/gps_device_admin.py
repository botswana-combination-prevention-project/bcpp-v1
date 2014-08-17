from django.contrib import admin
from edc.base.modeladmin.admin import BaseModelAdmin
from apps.bcpp_household.models import GpsDevice


class GpsDeviceAdmin(BaseModelAdmin):
    pass

admin.site.register(GpsDevice, GpsDeviceAdmin)
