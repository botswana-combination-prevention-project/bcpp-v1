from django.contrib import admin
from ..models import Pima
from ..forms import PimaForm
from .subject_visit_model_admin import SubjectVisitModelAdmin
from ..filters import Cd4ThreshHoldFilter


class PimaAdmin(SubjectVisitModelAdmin):

    form = PimaForm
    fields = (
        "subject_visit",
        'pima_today',
        'pima_today_other',
        'pima_today_other_other',
        'pima_id',
        'cd4_value',
        'cd4_datetime',
        )
    list_filter = ('subject_visit', 'cd4_datetime', 'pima_id', Cd4ThreshHoldFilter,)
    list_display = ('subject_visit', 'cd4_datetime', 'cd4_value', 'pima_id')
    radio_fields = {
        'pima_today': admin.VERTICAL,
        'pima_today_other': admin.VERTICAL}
admin.site.register(Pima, PimaAdmin)
