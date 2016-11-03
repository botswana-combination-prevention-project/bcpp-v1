from django.contrib import admin

from ..forms import HivUntestedForm
from ..models import HivUntested

from .subject_visit_model_admin import SubjectVisitModelAdmin


class HivUntestedAdmin(SubjectVisitModelAdmin):

    form = HivUntestedForm
    fields = (
        "subject_visit",
        'why_no_hiv_test',
        'hiv_pills',
        'arvs_hiv_test',)
    radio_fields = {
        "why_no_hiv_test": admin.VERTICAL,
        "hiv_pills": admin.VERTICAL,
        "arvs_hiv_test": admin.VERTICAL, }
admin.site.register(HivUntested, HivUntestedAdmin)
