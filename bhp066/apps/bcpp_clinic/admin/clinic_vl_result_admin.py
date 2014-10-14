from django.contrib import admin

from edc.base.modeladmin.admin import BaseModelAdmin

from ..forms import ClinicVLResultForm
from ..models import ClinicVLResult


class ClinicVLResultAdmin(BaseModelAdmin):

    form = ClinicVLResultForm
    list_display = ('clinician_initials', 'collection_datetime', 'result_value', 'site', 'validated_by')
    list_filter = ('clinician_initials', 'collection_datetime', 'result_value', 'site__site_name', )
    search_fields = ('clinician_initials', 'collection_datetime', 'result_value', 'site', )
admin.site.register(ClinicVLResult, ClinicVLResultAdmin)
