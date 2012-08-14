from django.contrib import admin
from bhp_base_model.classes import BaseModelAdmin
from models import LisImportError


class LisImportErrorAdmin(BaseModelAdmin):
    list_display = ('model_name', "identifier", 'created', "error_message")
    list_filter = ('model_name', 'created')
    search_fields = ("identifier", "error_message")
admin.site.register(LisImportError, LisImportErrorAdmin)
