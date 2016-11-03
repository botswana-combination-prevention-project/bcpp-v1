from django.contrib import admin

from edc.subject.registration.admin import BaseRegisteredSubjectModelAdmin

from bhp066.apps.bcpp_household_member.models import HouseholdMember

from ..forms import SubjectRefusalForm
from ..models import SubjectRefusal


class SubjectRefusalAdmin(BaseRegisteredSubjectModelAdmin):
    form = SubjectRefusalForm
    dashboard_type = 'subject'
    subject_identifier_attribute = 'registration_identifier'
    fields = (
        'household_member',
        'report_datetime',
        'refusal_date',
        'reason',
        'reason_other',
        'comment')

    radio_fields = {"reason": admin.VERTICAL}

    list_display = ('reason', )

    search_fields = [
        'household_member__first_name',
        'household_member__household_structure__household__household_identifier']

    list_filter = ('reason', 'household_member__household_structure__household__community')

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "household_member":
            kwargs["queryset"] = HouseholdMember.objects.filter(id__exact=request.GET.get('household_member', 0))
        return super(SubjectRefusalAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(SubjectRefusal, SubjectRefusalAdmin)
