from django.contrib import admin
from edc_lib.bhp_registration.admin import BaseRegisteredSubjectModelAdmin
from bcpp_household_member.models import HouseholdMember
from bcpp_subject.models import SubjectRefusal
from bcpp_subject.forms import SubjectRefusalForm


class SubjectRefusalAdmin(BaseRegisteredSubjectModelAdmin):
    form = SubjectRefusalForm
    dashboard_type = 'subject'
    subject_identifier_attribute = 'registration_identifier'
    fields = (
        'household_member',
        'report_datetime',
        'refusal_date',
        'why_no_participate',
        'why_no_participate_other',
        'comment')

    radio_fields = {
        "why_no_participate": admin.VERTICAL,
        }

    list_display = (
        'household_member',
        'why_no_participate')

    search_fields = [
        'household_member__first_name',
        'household_member__household_structure__household__household_identifier']

    list_filter = (
        'survey',
        'why_no_participate')

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "household_member":
            kwargs["queryset"] = HouseholdMember.objects.filter(id__exact=request.GET.get('household_member', 0))
        return super(SubjectRefusalAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(SubjectRefusal, SubjectRefusalAdmin)
