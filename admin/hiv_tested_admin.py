from django.contrib import admin
from subject_visit_model_admin import SubjectVisitModelAdmin
from bcpp_subject.models import HivTested
from bcpp_subject.forms import HivTestedForm


class HivTestedAdmin(SubjectVisitModelAdmin):

    form = HivTestedForm
    fields = (
        "subject_visit",
        'num_hiv_tests',
        'where_hiv_test',
        'why_hiv_test',
        'hiv_pills',
        'arvs_hiv_test',)
    radio_fields = {
        "where_hiv_test": admin.VERTICAL,
        "why_hiv_test": admin.VERTICAL,
        "hiv_pills": admin.VERTICAL,
        "arvs_hiv_test": admin.VERTICAL, }
admin.site.register(HivTested, HivTestedAdmin)
