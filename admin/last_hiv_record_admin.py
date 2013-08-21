from django.contrib import admin
from htc_visit_model_admin import HtcVisitModelAdmin
from bcpp_htc.models import LastHivRecord
from bcpp_htc.forms import LastHivRecordForm


class LastHivRecordAdmin(HtcVisitModelAdmin):

    form = LastHivRecordForm

    fields = (
        "htc_visit",
        "report_datetime",
        "recorded_test",
        "recorded_result",
        "attended_hiv_care",
        "hiv_care_clinic",
        "hiv_care_card")
    radio_fields = {
        "recorded_result": admin.VERTICAL,
        "attended_hiv_care": admin.VERTICAL,
        "hiv_care_card": admin.VERTICAL,}
admin.site.register(LastHivRecord, LastHivRecordAdmin)
