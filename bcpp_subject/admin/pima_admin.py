from django.contrib import admin
from bcpp_subject.models import Pima
from bcpp_subject.forms import PimaForm
from subject_visit_model_admin import SubjectVisitModelAdmin


class PimaAdmin(SubjectVisitModelAdmin):

    form = PimaForm
    fields = (
        "subject_visit",
        'pima_id',
        'cd4_value',
        'draw_time',
        'is_drawn',
        'is_drawn_other',)
    radio_fields = {
        'is_drawn': admin.VERTICAL}
admin.site.register(Pima, PimaAdmin)
