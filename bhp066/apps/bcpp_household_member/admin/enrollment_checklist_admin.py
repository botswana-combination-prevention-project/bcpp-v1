from django.contrib import admin

from edc.base.modeladmin.admin import BaseModelAdmin

from apps.bcpp_household.models import HouseholdStructure

from ..forms import EnrollmentChecklistForm
from ..models import EnrollmentChecklist, HouseholdMember


class EnrollmentChecklistAdmin(BaseModelAdmin):

    form = EnrollmentChecklistForm

    date_hierarchy = 'report_datetime'

    instructions = ['This form is a tool to assist the Interviewer to confirm the '
                    'Eligibility status of the subject. After entering the required items, click SAVE.']

    fields = (
        'household_member',
        'report_datetime',
        'initials',
        'dob',
        'gender',
        'has_identity',
        "citizen",
        "legal_marriage",
        "study_participation",
        "confirm_participation",
        "marriage_certificate",
        "part_time_resident",
        "household_residency",
        "literacy",
        "guardian",
        )

    list_display = ('household_member', 'report_datetime', 'gender', 'is_eligible', )

    list_filter = ('gender', 'is_eligible', 'report_datetime',
                   'household_member__household_structure__household__community')

    radio_fields = {
        'has_identity': admin.VERTICAL,
        "gender": admin.VERTICAL,
        "citizen": admin.VERTICAL,
        "legal_marriage": admin.VERTICAL,
        "marriage_certificate": admin.VERTICAL,
        "part_time_resident": admin.VERTICAL,
        "household_residency": admin.VERTICAL,
        "literacy": admin.VERTICAL,
        "guardian": admin.VERTICAL,
        "study_participation": admin.VERTICAL,
        "confirm_participation": admin.VERTICAL,
        }

    search_fields = ('household_member__first_name', 'household_member__pk')

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "household_structure":
            kwargs["queryset"] = HouseholdStructure.objects.filter(id__exact=request.GET.get('household_structure', 0))
        if db_field.name == "household_member":
            kwargs["queryset"] = HouseholdMember.objects.filter(id__exact=request.GET.get('household_member', 0))
        return super(EnrollmentChecklistAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(EnrollmentChecklist, EnrollmentChecklistAdmin)
