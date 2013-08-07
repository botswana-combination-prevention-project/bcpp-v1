from django.contrib import admin
from bhp_data_manager.models import ModelHelpText
from bhp_base_admin.admin import BaseModelAdmin


class ModelHelpTextAdmin(BaseModelAdmin):
    list_display = ('app_label', 'module_name', 'field_name', 'status')
    list_filter = ('app_label', 'module_name',)
admin.site.register(ModelHelpText, ModelHelpTextAdmin)
