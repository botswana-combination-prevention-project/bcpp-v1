from django.contrib import admin

from apps.bcpp_clinic.forms import ClinicMainForm

from .clinic_visit_model_admin import ClinicVisitModelAdmin
from ..models import ClinicMain


class ClinicMainAdmin(ClinicVisitModelAdmin):

    form = ClinicMainForm
    fields = (
        "clinic_visit",
        "report_datetime",
        "pims_id",
        "htc_id",
        "on_arv",
        "cd4_count",
    )
    radio_fields = {
        "on_arv": admin.VERTICAL}
admin.site.register(ClinicMain, ClinicMainAdmin)
