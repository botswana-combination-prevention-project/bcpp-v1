from django.contrib import admin

from ..models import ClinicQuestionnaire
from .clinic_visit_model_admin import ClinicVisitModelAdmin
from apps.bcpp_clinic.forms import ClinicQuestionnaireForm


class ClinicQuestionnaireAdmin(ClinicVisitModelAdmin):

    form = ClinicQuestionnaireForm
    fields = (
        "clinic_visit",
        'other_identifiers',
        'htc_and_or_pims',
        "report_datetime",
        "on_arv",
        "knows_last_cd4",
        "cd4_count",
    )
    radio_fields = {
        "on_arv": admin.VERTICAL,
        "knows_last_cd4": admin.VERTICAL,
        "other_identifiers": admin.VERTICAL}
    list_display = ('on_arv', 'cd4_count', 'report_datetime')
    list_filter = ('on_arv', 'other_identifiers', 'report_datetime')
    search_fields = (
        'on_arv', 'other_identifiers', 'htc_and_or_pims'
        )
admin.site.register(ClinicQuestionnaire, ClinicQuestionnaireAdmin)
