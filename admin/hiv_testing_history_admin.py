from django.contrib import admin
from subject_visit_model_admin import SubjectVisitModelAdmin
from bcpp_subject.models import HivTestingHistory
from bcpp_subject.forms import HivTestingHistoryForm


class HivTestingHistoryAdmin(SubjectVisitModelAdmin):

    form = HivTestingHistoryForm
    fields = (
        "subject_visit",
        'has_tested',
        "when_hiv_test",
        'has_record',
        'verbal_hiv_result',
        'other_record',)
    radio_fields = {
        "has_tested": admin.VERTICAL,
        "has_record": admin.VERTICAL,
        "verbal_hiv_result": admin.VERTICAL,
        'other_record': admin.VERTICAL,}
admin.site.register(HivTestingHistory, HivTestingHistoryAdmin)
