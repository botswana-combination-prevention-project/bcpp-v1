from django.contrib import admin
from htc_visit_model_admin import HtcVisitModelAdmin
from bcpp_htc.models import DemographicsRisk
from bcpp_htc.forms import DemographicsRiskForm


class DemographicsRiskAdmin(HtcVisitModelAdmin):

    form = DemographicsRiskForm

    fields = (
        "htc_visit",
        "report_datetime",
        "education",
        "employment",
        "marital_status",
        "alcohol_intake",
    )
    radio_fields = {
        "education": admin.VERTICAL,
        "employment": admin.VERTICAL,
        "marital_status": admin.VERTICAL,
        "alcohol_intake": admin.VERTICAL}
admin.site.register(DemographicsRisk, DemographicsRiskAdmin)
