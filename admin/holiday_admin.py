from django.contrib import admin
from bhp_base_model.classes import BaseModelAdmin
from bhp_common.models import MyTabularInline
from bhp_appointment.models import Holiday


class HolidayAdmin(BaseModelAdmin):
    pass
admin.site.register(Holiday, HolidayAdmin)


class HolidayInlineAdmin(MyTabularInline):
    model = Holiday
    extra = 0
