from django.contrib import admin
from bhp_data_manager.models import ModelHelpText
from bhp_base_admin.admin import BaseModelAdmin


class ModelHelpTextAdmin(BaseModelAdmin):
    pass
admin.site.register(ModelHelpText, ModelHelpTextAdmin)
