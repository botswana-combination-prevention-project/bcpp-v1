from django.contrib import admin
from ..models import Pima
from ..forms import PimaForm
from .subject_visit_model_admin import SubjectVisitModelAdmin


class PimaAdmin(SubjectVisitModelAdmin):

    form = PimaForm
    fields = (
        "subject_visit",
        'pima_today',
        'pima_today_other',
        'pima_id',
        'cd4_value',
        'cd4_datetime',
        )
    radio_fields = {
        'pima_today': admin.VERTICAL}
admin.site.register(Pima, PimaAdmin)
