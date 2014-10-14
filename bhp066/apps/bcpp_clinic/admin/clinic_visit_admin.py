from django.contrib import admin

from ..forms import ClinicVisitForm
from ..models import ClinicVisit
from apps.bcpp_clinic_lab.models import ClinicRequisition

from edc.subject.appointment.admin import BaseAppointmentModelAdmin


class ClinicVisitAdmin(BaseAppointmentModelAdmin):

    form = ClinicVisitForm
    visit_model_instance_field = 'clinic_visit'
    requisition_model = ClinicRequisition
    dashboard_type = 'clinic'

    list_display = (
        'appointment',
        'report_datetime',
        'reason',
        "info_source",
        'created',
        'user_created',
    )

    list_filter = (
        'report_datetime',
        'reason',
        'appointment__appt_status',
        'appointment__visit_definition__code',
        )

    search_fields = (
        'appointment__registered_subject__subject_identifier',
        'appointment__registered_subject__registration_identifier',
        'appointment__registered_subject__first_name',
        'appointment__registered_subject__identity',
        )

    fields = (
        "appointment",
        "report_datetime",
        "reason",
        "comments"
        )
admin.site.register(ClinicVisit, ClinicVisitAdmin)
