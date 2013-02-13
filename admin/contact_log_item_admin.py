from django.contrib import admin
from bhp_base_model.classes import BaseModelAdmin
from bhp_common.models import MyTabularInline
from bhp_appointment.models import ContactLogItem
from bhp_appointment.forms import ContactLogItemForm


class ContactLogItemInlineAdmin(MyTabularInline):
    model = ContactLogItem
    form = ContactLogItemForm
    extra = 1


class ContactLogItemAdmin(BaseModelAdmin):
    form = ContactLogItemForm
admin.site.register(ContactLogItem, ContactLogItemAdmin)
