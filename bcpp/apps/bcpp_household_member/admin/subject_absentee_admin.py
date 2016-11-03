from django.contrib import admin

from edc_base.modeladmin.admin import BaseModelAdmin, BaseTabularInline
from edc.subject.registration.admin import BaseRegisteredSubjectModelAdmin

from ..forms import SubjectAbsenteeEntryForm
from ..models import HouseholdMember, SubjectAbsentee, SubjectAbsenteeEntry


class SubjectAbsenteeEntryAdmin(BaseModelAdmin):

    fields = (
        'subject_absentee',
        'report_datetime',
        'next_appt_datetime',
        'next_appt_datetime_source',
        'reason',
        'reason_other',
        'contact_details')

    list_display = (
        'subject_absentee',
        'report_datetime',
        'next_appt_datetime',
        'contact_details')

    radio_fields = {
        "reason": admin.VERTICAL,
        "next_appt_datetime_source": admin.VERTICAL}

    list_filter = ('report_datetime', 'subject_absentee__household_member__household_structure__household__community')

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
        'next_appt_datetime_source',)
    form = SubjectAbsenteeEntryForm
    model = SubjectAbsenteeEntry
    max_num = 3
    extra = 1


class SubjectAbsenteeAdmin(BaseRegisteredSubjectModelAdmin):

    form = SubjectAbsenteeEntryForm
    inlines = [SubjectAbsenteeEntryInline, ]

    dashboard_type = 'subject'

    subject_identifier_attribute = 'registration_identifier'

    search_fields = ['household_member__first_name',
                     'household_member__household_structure__household__household_identifier', ]
    list_display = ['household_member',
                    'survey',
                    'report_datetime']
    list_filter = ['survey',
                   'report_datetime',
                   'hostname_created']
    fields = (
        'registered_subject',
        'household_member',
        'report_datetime')

    readonly_fields = (
        'registered_subject',
        'household_member',
        'survey',
        'report_datetime',)
    instructions = []

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "household_member":
            kwargs["queryset"] = HouseholdMember.objects.filter(id__exact=request.GET.get('household_member', 0))
        return super(SubjectAbsenteeAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(SubjectAbsentee, SubjectAbsenteeAdmin)
