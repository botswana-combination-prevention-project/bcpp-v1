from django.contrib import admin

from edc_base.modeladmin.mixins import TabularInlineMixin

from ..admin_site import bcpp_household_member_admin
from ..forms import SubjectUndecidedForm, SubjectUndecidedEntryForm
from ..models import SubjectUndecided, SubjectUndecidedEntry

from .modeladmin_mixins import HouseholdMemberAdminMixin


@admin.register(SubjectUndecidedEntry, site=bcpp_household_member_admin)
class SubjectUndecidedEntryAdmin(HouseholdMemberAdminMixin, admin.ModelAdmin):

    fields = (
        'subject_undecided',
        'report_datetime',
        'next_appt_datetime',
        'next_appt_datetime_source',
        'subject_undecided_reason',
        'reason_other',
        'contact_details')

    list_display = (
        'subject_undecided',
        'report_datetime',
        'next_appt_datetime',
        'contact_details')

    radio_fields = {
        "subject_undecided_reason": admin.VERTICAL,
        "next_appt_datetime_source": admin.VERTICAL}

    list_filter = ('report_datetime', 'subject_undecided__household_member__household_structure__household__community')

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "subject_undecided":
            kwargs["queryset"] = SubjectUndecided.objects.filter(id__exact=request.GET.get('subject_undecided', 0))
        return super(SubjectUndecidedEntryAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(SubjectUndecidedEntry, SubjectUndecidedEntryAdmin)


class SubjectUndecidedEntryInline(TabularInlineMixin, admin.TabularInline):
    form = SubjectUndecidedEntryForm
    model = SubjectUndecidedEntry
    max_num = 2
    extra = 1


@admin.register(SubjectUndecided, site=bcpp_household_member_admin)
class SubjectUndecidedAdmin(HouseholdMemberAdminMixin, admin.ModelAdmin):

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
    instructions = []
