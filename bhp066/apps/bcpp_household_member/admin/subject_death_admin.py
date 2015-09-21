from django.contrib import admin

from edc.subject.registration.admin import BaseRegisteredSubjectModelAdmin

from bhp066.apps.bcpp_household_member.models import HouseholdMember

from ..forms import SubjectDeathForm
from ..models import SubjectDeath


class SubjectDeathAdmin(BaseRegisteredSubjectModelAdmin):
    form = SubjectDeathForm

    fields = (
        'household_member',
        'report_datetime',
        'death_date',
        'site_aware_date',
        'death_cause_info',
        'death_cause_info_other',
        'death_cause',
        'death_cause_category',
        'death_cause_other',
        'duration_of_illness',
        'primary_medical_care_giver',
        'relationship_death_study')

    list_display = ('household_member', 'report_datetime')

    search_fields = [
        'household_member__first_name',
        'household_member__registered_subject__subject_identifier',
        'household_member__household_structure__household__household_identifier']

    list_filter = ('report_datetime', 'household_member__household_structure__household__community')

    radio_fields = {
        "death_cause_info": admin.VERTICAL,
        "death_cause_category": admin.VERTICAL,
        "primary_medical_care_giver": admin.VERTICAL,
        "relationship_death_study": admin.VERTICAL
    }

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "household_member":
            kwargs["queryset"] = HouseholdMember.objects.filter(id__exact=request.GET.get('household_member', 0))
        return super(SubjectDeathAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(SubjectDeath, SubjectDeathAdmin)
