from django.contrib import admin

from edc.subject.registration.admin import BaseRegisteredSubjectModelAdmin

from bhp066.apps.bcpp_household_member.models import HouseholdMember

from ..forms import SubjectMovedForm
from ..models import SubjectMoved


class SubjectMovedAdmin(BaseRegisteredSubjectModelAdmin):
    form = SubjectMovedForm
    dashboard_type = 'subject'
    subject_identifier_attribute = 'registration_identifier'

    fields = (
        'household_member',
        'report_datetime',
        'moved_household',
        'moved_community',
        'new_community',
        'update_locator',
        'comment')
    list_display = (
        'household_member',
        'moved_household',
        'moved_community',
        'new_community',
        'update_locator',
    )
    search_fields = [
        'household_member__first_name',
        'household_member__household_structure__household__household_identifier']
    list_filter = ('survey', 'household_member__household_structure__household__community')
    radio_fields = {
        "moved_household": admin.VERTICAL,
        "moved_community": admin.VERTICAL,
        "update_locator": admin.VERTICAL,
    }

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "household_member":
            kwargs["queryset"] = HouseholdMember.objects.filter(id__exact=request.GET.get('HouseholdMember', 0))
        return super(SubjectMovedAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(SubjectMoved, SubjectMovedAdmin)
