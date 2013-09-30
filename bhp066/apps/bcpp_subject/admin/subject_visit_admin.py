from django.contrib import admin
from edc.subject.appointment.admin import BaseAppointmentModelAdmin
from apps.bcpp_lab.models import SubjectRequisition
from apps.bcpp_household_member.models import HouseholdMember
from ..models import SubjectVisit
from ..forms import SubjectVisitForm


class SubjectVisitAdmin(BaseAppointmentModelAdmin):

    form = SubjectVisitForm
    visit_model_instance_field = 'subject_visit'
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

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "household_member":
            household_members = HouseholdMember.objects.none()
            if HouseholdMember.objects.filter(id=request.GET.get('household_member', 0)):
                household_members = HouseholdMember.objects.filter(id=request.GET.get('household_member', 0))
            kwargs["queryset"] = household_members
        return super(SubjectVisitAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(SubjectVisit, SubjectVisitAdmin)
