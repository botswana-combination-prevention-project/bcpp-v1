from django.contrib import admin

from edc.base.modeladmin.admin import BaseModelAdmin

from ..models import AliquotType


class AliquotTypeAdmin(BaseModelAdmin):

    list_display = ('name', 'alpha_code', 'numeric_code')

admin.site.register(AliquotType, AliquotTypeAdmin)
