
from django.contrib import admin
from bhp_base_model.classes import BaseModelAdmin
from bhp_common.models import MyTabularInline
from bhp_appointment.forms import PreAppointmentContactForm
from bhp_appointment.models import PreAppointmentContact


class PreAppointmentContactInlineAdmin(MyTabularInline):
    model = PreAppointmentContact
    form = PreAppointmentContactForm
    extra = 1
    radio_fields = {"is_contacted": admin.VERTICAL,
                    "is_confirmed": admin.VERTICAL}


class PreAppointmentContactAdmin(BaseModelAdmin):
    form = PreAppointmentContactForm
    radio_fields = {"is_contacted": admin.VERTICAL,
                    "is_confirmed": admin.VERTICAL}
admin.site.register(PreAppointmentContact, PreAppointmentContactAdmin)
