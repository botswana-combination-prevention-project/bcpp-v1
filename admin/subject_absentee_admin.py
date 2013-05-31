from django.contrib import admin
from bhp_base_admin.admin import BaseModelAdmin, BaseTabularInline
from bhp_registration.admin import BaseRegisteredSubjectModelAdmin
from bcpp_household.models import HouseholdStructureMember
from bcpp_subject.forms import SubjectAbsenteeEntryForm
from bcpp_subject.models import SubjectAbsentee, SubjectAbsenteeEntry


class SubjectAbsenteeEntryAdmin(BaseModelAdmin):

    list_display = (
        'id', 
        'subject_absentee', 
        'report_datetime',)
    radio_fields = {
        "subject_absentee_reason": admin.VERTICAL,
        "next_appt_datetime_source": admin.VERTICAL}

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "subject_absentee":
            kwargs["queryset"] = SubjectAbsentee.objects.filter(id__exact=request.GET.get('subject_absentee', 0))
        return super(SubjectAbsenteeEntryAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(SubjectAbsenteeEntry, SubjectAbsenteeEntryAdmin)


class SubjectAbsenteeEntryInline(BaseTabularInline):
    fields = (
        'report_datetime', 
        'reason', 
        'reason_other', 
        'next_appt_datetime', 
        'next_appt_datetime_source')
    form = SubjectAbsenteeEntryForm
    model = SubjectAbsenteeEntry
    max_num = 3
    extra = 1


class SubjectAbsenteeAdmin(BaseRegisteredSubjectModelAdmin):

    form = SubjectAbsenteeEntryForm
    inlines = [SubjectAbsenteeEntryInline, ]

    dashboard_type = 'subject'
    subject_identifier_attribute = 'registration_identifier'
    fields = (
        'registered_subject',
        'household_structure_member',
        'report_datetime',
        )
    list_display = (
        'household_structure_member', 
        'survey', 
        'subject_absentee_status', 
        'report_datetime',)
    list_filter = (
        'survey', 
        'report_datetime', 
        'hostname_created',)
    search_fields = [
        'household_structure_member__first_name', 
        'household_structure_member__household_structure__household__household_identifier', ]
    readonly_fields = (
        'registered_subject', 
        'household_structure_member', 
        'survey', 
        'subject_absentee_status', 
        'report_datetime',)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "household_structure_member":
            kwargs["queryset"] = HouseholdStructureMember.objects.filter(id__exact=request.GET.get('household_structure_member', 0))
        return super(SubjectAbsenteeAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(SubjectAbsentee, SubjectAbsenteeAdmin)
