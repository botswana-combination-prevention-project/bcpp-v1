from django.contrib import admin
from bhp_appointment.admin import BaseAppointmentModelAdmin
from bcpp_lab.models import SubjectRequisition
from bcpp_htc.models import HtcVisit
from bcpp_htc.forms import HtcVisitForm


class HtcVisitAdmin(BaseAppointmentModelAdmin):

    form = HtcVisitForm
    visit_model_instance_field = 'htc_visit'
    requisition_model = SubjectRequisition
    dashboard_type = 'subject'

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
        'household_member',
        "appointment",
        "report_datetime",
        "comments"
        )

admin.site.register(HtcVisit, HtcVisitAdmin)
