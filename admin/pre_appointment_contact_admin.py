from django.contrib import admin
from bhp_base_admin.admin import BaseModelAdmin
from bhp_base_admin.admin import BaseTabularInline
from bhp_appointment.forms import PreAppointmentContactForm
from bhp_appointment.models import PreAppointmentContact


class PreAppointmentContactInlineAdmin(BaseTabularInline):
    model = PreAppointmentContact
    form = PreAppointmentContactForm
    extra = 0
    fields = ('contact_datetime', 'is_contacted', 'information_provider', 'is_confirmed', 'comment')
    radio_fields = {"is_contacted": admin.VERTICAL}


class PreAppointmentContactAdmin(BaseModelAdmin):
    form = PreAppointmentContactForm
    date_hierarchy = 'contact_datetime'
    fields = ('contact_datetime', 'is_contacted', 'information_provider', 'is_confirmed', 'comment')
    list_display = ('appointment', 'contact_datetime', 'is_contacted', 'information_provider', 'is_confirmed')
    list_filter = ('contact_datetime', 'is_contacted', 'information_provider', 'is_confirmed')
    search_fields = ('appointment__registered_subject__subject_identifier', 'id', 'appointment__pk')
    radio_fields = {"is_contacted": admin.VERTICAL}
admin.site.register(PreAppointmentContact, PreAppointmentContactAdmin)
