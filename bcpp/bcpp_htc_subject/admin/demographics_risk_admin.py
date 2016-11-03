from django.contrib import admin
from htc_subject_visit_model_admin import HtcSubjectVisitModelAdmin
from ..models import DemographicsRisk
from ..forms import DemographicsRiskForm


class DemographicsRiskAdmin(HtcSubjectVisitModelAdmin):

    form = DemographicsRiskForm

    fields = (
        "htc_subject_visit",
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
