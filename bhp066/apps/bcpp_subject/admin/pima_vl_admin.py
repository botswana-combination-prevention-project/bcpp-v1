from django.contrib import admin
from ..models import PimaVl
from ..forms import PimaVlForm
from .subject_visit_model_admin import SubjectVisitModelAdmin
from ..filters import Cd4ThreshHoldFilter


class PimaVlAdmin(SubjectVisitModelAdmin):

    form = PimaVlForm
    fields = (
        "subject_visit",
        'poc_vl_today',
        'poc_vl_today_other',
        'poc_today_vl_other_other',
        'pima_id',
        'cd4_value',
        'time_of_test',
        'time_of_result',
        'easy_of_use',
        'stability',
        )
    exclude = ('poc_vl_type',)
    list_filter = ('subject_visit', 'time_of_test', 'pima_id', Cd4ThreshHoldFilter,)
    list_display = ('subject_visit', 'time_of_test', 'cd4_value', 'pima_id')
    radio_fields = {
        'poc_vl_today': admin.VERTICAL,
        'easy_of_use': admin.VERTICAL}

    def save_model(self, request, obj, form, change):
        self.obj.valid_user(self, request.user)

admin.site.register(PimaVl, PimaVlAdmin)
