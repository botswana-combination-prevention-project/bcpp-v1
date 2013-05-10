from django.contrib import admin
from bhp_base_admin.admin import BaseModelAdmin
from bhp_appointment.models import Configuration
from holiday_admin import HolidayInlineAdmin


class ConfigurationAdmin(BaseModelAdmin):
    inlines = [HolidayInlineAdmin, ]
admin.site.register(Configuration, ConfigurationAdmin)
