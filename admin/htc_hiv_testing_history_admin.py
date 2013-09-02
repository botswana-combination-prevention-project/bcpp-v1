from django.contrib import admin
from htc_subject_visit_model_admin import HtcSubjectVisitModelAdmin
from bcpp_htc.models import HtcHivTestingHistory
from bcpp_htc.forms import HtcHivTestingHistoryForm


class HtcHivTestingHistoryAdmin(HtcSubjectVisitModelAdmin):

    form = HtcHivTestingHistoryForm

    fields = (
        "htc_visit",
        "report_datetime",
        "previous_testing",
        "testing_place",
        "hiv_record",
        "result_obtained",)
    radio_fields = {
        "previous_testing": admin.VERTICAL,
        "testing_place": admin.VERTICAL,
        "hiv_record": admin.VERTICAL,
        "result_obtained": admin.VERTICAL}
admin.site.register(HtcHivTestingHistory, HtcHivTestingHistoryAdmin)
