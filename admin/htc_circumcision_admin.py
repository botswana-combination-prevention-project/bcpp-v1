from django.contrib import admin
from htc_visit_model_admin import HtcVisitModelAdmin
from bcpp_htc.models import HtcCircumcision
from bcpp_htc.forms import HtcCircumcisionForm


class HtcCircumcisionAdmin(HtcVisitModelAdmin):

    form = HtcCircumcisionForm

    fields = (
        "htc_visit",
        "report_datetime",
        "is_circumcised",
        "circumcision_year",)
    radio_fields = {
        "is_circumcised": admin.VERTICAL,}
admin.site.register(HtcCircumcision, HtcCircumcisionAdmin)
