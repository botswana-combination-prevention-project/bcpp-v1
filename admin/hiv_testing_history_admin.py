from django.contrib import admin
from htc_visit_model_admin import HtcVisitModelAdmin
from bcpp_htc.models import HivTestingHistory
from bcpp_htc.forms import HivTestingHistoryForm


class HivTestingHistoryAdmin(HtcVisitModelAdmin):

    form = HivTestingHistoryForm

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
        "result_obtained": admin.VERTICAL,}
admin.site.register(HivTestingHistory, HivTestingHistoryAdmin)
