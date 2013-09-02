from django.contrib import admin
from htc_subject_visit_model_admin import HtcSubjectVisitModelAdmin
from bcpp_subject_htc.models import DemographicsRisk
from bcpp_subject_htc.forms import DemographicsRiskForm


class DemographicsRiskAdmin(HtcSubjectVisitModelAdmin):

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
