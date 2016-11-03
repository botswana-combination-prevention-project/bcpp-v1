from django.contrib import admin

from ..forms import ClinicQuestionnaireForm
from ..models import ClinicQuestionnaire

from .subject_visit_model_admin import SubjectVisitModelAdmin


class ClinicQuestionnaireAdmin(SubjectVisitModelAdmin):

    form = ClinicQuestionnaireForm
    fields = (
        "subject_visit",
        "report_datetime",
        "know_hiv_status",
        "current_hiv_status",
        "on_arv",
        "arv_evidence",
    )
    radio_fields = {
        "know_hiv_status": admin.VERTICAL,
        "current_hiv_status": admin.VERTICAL,
        "on_arv": admin.VERTICAL,
        "arv_evidence": admin.VERTICAL}

admin.site.register(ClinicQuestionnaire, ClinicQuestionnaireAdmin)
