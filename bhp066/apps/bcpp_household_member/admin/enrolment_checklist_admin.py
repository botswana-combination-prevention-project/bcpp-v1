from django.contrib import admin

from edc.base.admin.admin import BaseModelAdmin

from apps.bcpp_household.models import HouseholdStructure

from ..forms import EnrolmentChecklistForm
from ..models import EnrolmentChecklist, HouseholdMember


class EnrolmentChecklistAdmin(BaseModelAdmin):

    form = EnrolmentChecklistForm

    instructions = ['This form is a tool to assist the Interviewer to confirm the Eligibility status of the subject. After entering the required items, click SAVE. THE DATA WILL BE EVALUATED BUT NOT SAVED.']

    fields = (
        'household_member',
        'initials',
        'dob',
        'gender',
        'has_identity',
        "citizen",
        "legal_marriage",
        "marriage_certificate",
        "part_time_resident",
        "literacy",
        "guardian",
        )

    list_display = ('household_member', 'is_eligible', )

    radio_fields = {
        'has_identity': admin.VERTICAL,
        "gender": admin.VERTICAL,
        "citizen": admin.VERTICAL,
        "legal_marriage": admin.VERTICAL,
        "marriage_certificate": admin.VERTICAL,
        "part_time_resident": admin.VERTICAL,
        "literacy": admin.VERTICAL,
        "guardian": admin.VERTICAL,
        }

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "household_structure":
            kwargs["queryset"] = HouseholdStructure.objects.filter(id__exact=request.GET.get('household_structure', 0))
        if db_field.name == "household_member":
            kwargs["queryset"] = HouseholdMember.objects.filter(id__exact=request.GET.get('household_member', 0))
        return super(EnrolmentChecklistAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(EnrolmentChecklist, EnrolmentChecklistAdmin)
