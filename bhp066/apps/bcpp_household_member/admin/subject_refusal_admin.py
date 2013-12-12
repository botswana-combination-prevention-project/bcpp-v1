from django.contrib import admin
from edc.subject.registration.admin import BaseRegisteredSubjectModelAdmin
from apps.bcpp_household_member.models import HouseholdMember
from ..models import SubjectRefusal
from ..forms import SubjectRefusalForm


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
        'participant_offered_htc',
        'comment')

    radio_fields = {
        "why_no_participate": admin.VERTICAL,
        }

    list_display = (
        'why_no_participate',
        'participant_offered_htc')

    search_fields = [
        'household_member__first_name',
        'household_member__household_structure__household__household_identifier',
        'participant_offered_htc']

    list_filter = (
        'why_no_participate',
        'participant_offered_htc')

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "household_member":
            kwargs["queryset"] = HouseholdMember.objects.filter(id__exact=request.GET.get('household_member', 0))
        return super(SubjectRefusalAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(SubjectRefusal, SubjectRefusalAdmin)
