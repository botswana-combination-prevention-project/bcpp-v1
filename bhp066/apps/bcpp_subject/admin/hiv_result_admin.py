from django.contrib import admin

from ..filters import HivResultFilter
from ..forms import HivResultForm
from ..models import HivResult

from .subject_visit_model_admin import SubjectVisitModelAdmin


class HivResultAdmin (SubjectVisitModelAdmin):

    form = HivResultForm
    fields = (
        'subject_visit',
        'hiv_result',
        'hiv_result_datetime',
        'blood_draw_type',
        'insufficient_vol',
        'why_not_tested',)

    list_filter = (HivResultFilter,)

    radio_fields = {
        "hiv_result": admin.VERTICAL,
        "blood_draw_type": admin.VERTICAL,
        "insufficient_vol": admin.VERTICAL,
        'why_not_tested': admin.VERTICAL, }
admin.site.register(HivResult, HivResultAdmin)
