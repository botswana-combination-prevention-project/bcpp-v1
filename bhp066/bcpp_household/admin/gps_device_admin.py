from django.contrib import admin
from edc.base.admin.admin import BaseModelAdmin
from bcpp_household.models import GpsDevice


class GpsDeviceAdmin(BaseModelAdmin):
    pass

admin.site.register(GpsDevice, GpsDeviceAdmin)
