from django.contrib import admin
from subject_visit_model_admin import SubjectVisitModelAdmin
from bcpp_subject.models import HivResult
from bcpp_subject.forms import HivResultForm


class HivResultAdmin (SubjectVisitModelAdmin):

    form = HivResultForm
    fields = (
        'subject_visit',
        'hiv_result',
        'hiv_result_datetime',
        'why_not_tested',)
    radio_fields = {
        "hiv_result": admin.VERTICAL,
        'why_not_tested': admin.VERTICAL, }
admin.site.register(HivResult, HivResultAdmin)
