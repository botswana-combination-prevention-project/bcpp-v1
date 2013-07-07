from django.contrib import admin
from bhp_base_admin.admin import BaseModelAdmin
from bhp_supplemental_fields.models import Excluded


class ExcludedAdmin(BaseModelAdmin):
    list_display = ('id', 'app_label', 'object_name', 'created', 'modified')
    list_filter = ('app_label', 'object_name')
admin.site.register(Excluded, ExcludedAdmin)
