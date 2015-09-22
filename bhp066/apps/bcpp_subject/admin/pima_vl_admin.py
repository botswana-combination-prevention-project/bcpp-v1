from django.contrib import admin

from ..models import PimaVl
from ..forms import PimaVlForm

from .subject_visit_model_admin import SubjectVisitModelAdmin


class PimaVlAdmin(SubjectVisitModelAdmin):

    form = PimaVlForm
    fields = (
        "subject_visit",
        'poc_vl_today',
        'poc_vl_today_other',
        'poc_today_vl_other_other',
        'pima_id',
        'vl_value_quatifier',
        'poc_vl_value',
        'time_of_test',
        'time_of_result',
        'easy_of_use',
        'stability',
        'confirmation_code',
    )
    exclude = ('poc_vl_type', 'quota_pk')
    list_filter = ('subject_visit', 'time_of_test', 'pima_id')
    list_display = ('subject_visit', 'time_of_test', 'poc_vl_value', 'pima_id', 'pre_order')
    radio_fields = {
        'poc_vl_today': admin.VERTICAL,
        'poc_vl_today_other': admin.VERTICAL,
        'vl_value_quatifier': admin.VERTICAL,
        'easy_of_use': admin.VERTICAL}

admin.site.register(PimaVl, PimaVlAdmin)
