from django.contrib import admin

from edc_base.modeladmin.admin import BaseModelAdmin

from ..filters import ClinicCommunityListFilter
from ..forms import ClinicVlResultForm
from ..models import ClinicVlResult


class ClinicVlResultAdmin(BaseModelAdmin):

    form = ClinicVlResultForm
    fields = (
        'clinic_visit',
        'report_datetime',
        'site',
        'clinician_initials',
        'collection_datetime',
        'assay_date',
        'result_value',
        'comment',
        'validation_date',
        'validated_by')

    list_display = ('clinic_visit', 'clinician_initials', 'collection_datetime', 'result_value', 'validated_by')
    list_filter = ('collection_datetime', ClinicCommunityListFilter, )
    search_fields = ('clinic_visit__appointment__registered_subject__subject_identifier', 'clinician_initials', 'result_value', )
admin.site.register(ClinicVlResult, ClinicVlResultAdmin)
