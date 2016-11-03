from django.contrib import admin

from ..forms import TbSymptomsForm
from ..models import TbSymptoms

from .subject_visit_model_admin import SubjectVisitModelAdmin


class TbSymptomsAdmin(SubjectVisitModelAdmin):

    form = TbSymptomsForm
    fields = (
        "subject_visit",
        'cough',
        'fever',
        'lymph_nodes',
        'cough_blood',
        'night_sweat',
        'weight_loss',)
    radio_fields = {
        "cough": admin.VERTICAL,
        "fever": admin.VERTICAL,
        "lymph_nodes": admin.VERTICAL,
        "night_sweat": admin.VERTICAL,
        "weight_loss": admin.VERTICAL,
        "cough_blood": admin.VERTICAL, }
admin.site.register(TbSymptoms, TbSymptomsAdmin)
