
from django.contrib import admin
from bhp_base_model.classes import BaseModelAdmin
from bhp_common.models import MyTabularInline
from bhp_appointment.forms import PreAppointmentContactForm
from bhp_appointment.models import PreAppointmentContact


class PreAppointmentContactInlineAdmin(MyTabularInline):
    model = PreAppointmentContact
    form = PreAppointmentContactForm
    extra = 1
    fields = ('contact_datetime', 'is_contacted', 'information_provider', 'is_confirmed', 'comment')
    radio_fields = {"is_contacted": admin.VERTICAL,
                    "is_confirmed": admin.VERTICAL}


class PreAppointmentContactAdmin(BaseModelAdmin):
    form = PreAppointmentContactForm
    date_hierarchy = 'contact_datetime'
    fields = ('contact_datetime', 'is_contacted', 'information_provider', 'is_confirmed', 'comment')
    list_display = ('appointment', 'contact_datetime', 'is_contacted', 'information_provider', 'is_confirmed')
    list_filter = ('contact_datetime', 'is_contacted', 'information_provider', 'is_confirmed')
    search_fields = ('appointment__registered_subject__subject_identifier', 'id')
    radio_fields = {"is_contacted": admin.VERTICAL,
                    "is_confirmed": admin.VERTICAL}
admin.site.register(PreAppointmentContact, PreAppointmentContactAdmin)
