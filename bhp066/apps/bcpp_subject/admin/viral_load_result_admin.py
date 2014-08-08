from django.contrib import admin
from django.utils.translation import ugettext as _
from edc.base.admin.admin import BaseModelAdmin

from ..models import ViralLoadResult
from ..forms import ViralLoadResultForm


class ViralLoadResultAdmin(BaseModelAdmin):

    form = ViralLoadResultForm
    list_display = ('registered_subject', 'sample_id', 'clinician_initials', 'collection_datetime', 'result_value', 'clinic', 'assay_performed_by', 'validated_by')
    list_filter = ('clinician_initials', 'collection_datetime', 'report_datetime', 'result_value', 'clinic__site_name', )
    search_fields = ('registered_subject', 'sample_id', 'clinician_initials', 'collection_datetime', 'result_value', 'clinic', )
admin.site.register(ViralLoadResult, ViralLoadResultAdmin)