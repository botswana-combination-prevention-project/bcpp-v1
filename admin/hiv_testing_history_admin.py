from django.contrib import admin
from subject_visit_model_admin import SubjectVisitModelAdmin
from bcpp_subject.models import HivTestingHistory
from bcpp_subject.forms import HivTestingHistoryForm


# HivTestingHistory
class HivTestingHistoryAdmin(SubjectVisitModelAdmin):

    form = HivTestingHistoryForm
    fields = (
        "subject_visit",
        'take_hiv_testing',
        'why_not_tested',
        'has_tested',
        'has_record',
        "when_hiv_test",
        'verbal_hiv_result',)
    radio_fields = {
        "take_hiv_testing": admin.VERTICAL,
        "why_not_tested": admin.VERTICAL,
        "has_tested": admin.VERTICAL,
        "has_record": admin.VERTICAL,
        "verbal_hiv_result": admin.VERTICAL,}
admin.site.register(HivTestingHistory, HivTestingHistoryAdmin)