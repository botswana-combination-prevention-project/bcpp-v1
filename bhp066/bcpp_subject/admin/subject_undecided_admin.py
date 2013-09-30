from django.contrib import admin
from edc.core.bhp_base_admin.admin import BaseModelAdmin, BaseTabularInline
from edc.core.bhp_registration.admin import BaseRegisteredSubjectModelAdmin
from bcpp_household_member.models import HouseholdMember
from ..models import SubjectUndecided, SubjectUndecidedEntry
from ..forms import SubjectUndecidedForm, SubjectUndecidedEntryForm


class SubjectUndecidedEntryAdmin(BaseModelAdmin):

    list_display = (
        'id',
        'subject_undecided',
        'report_datetime',)
    radio_fields = {
        "subject_undecided_reason": admin.VERTICAL,
        "next_appt_datetime_source": admin.VERTICAL}

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "subject_undecided":
            kwargs["queryset"] = SubjectUndecided.objects.filter(id__exact=request.GET.get('subject_undecided', 0))
        return super(SubjectUndecidedEntryAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(SubjectUndecidedEntry, SubjectUndecidedEntryAdmin)


class SubjectUndecidedEntryInline(BaseTabularInline):
    form = SubjectUndecidedEntryForm
    model = SubjectUndecidedEntry
    max_num = 2
    extra = 1


class SubjectUndecidedAdmin(BaseRegisteredSubjectModelAdmin):

    form = SubjectUndecidedForm
    inlines = [SubjectUndecidedEntryInline, ]

    dashboard_type = 'subject'

    subject_identifier_attribute = 'registration_identifier'

    fields = (
              'registered_subject',
              'household_member',
              'report_datetime')

    list_display = (
            'household_member',
            'report_datetime')

    search_fields = [
            'household_member__first_name',
            'household_member__household_structure__household__household_identifier', ]

    list_filter = ('survey',)

    readonly_fields = (
            'registered_subject',
            'household_member',
            'survey',
            'report_datetime',)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "household_member":
            kwargs["queryset"] = HouseholdMember.objects.filter(id__exact=request.GET.get('household_member', 0))
            return super(SubjectUndecidedAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(SubjectUndecided, SubjectUndecidedAdmin)
