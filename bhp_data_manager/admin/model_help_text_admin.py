from django.contrib import admin
from bhp_data_manager.models import ModelHelpText
from bhp_base_admin.admin import BaseModelAdmin
from bhp_data_manager.forms import  ModelHelpTextForm


class ModelHelpTextAdmin(BaseModelAdmin):
    form = ModelHelpTextForm
    list_display = ('app_label', 'module_name', 'field_name', 'url', 'status')
    list_filter = ('app_label', 'module_name',)
admin.site.register(ModelHelpText, ModelHelpTextAdmin)
