from django.contrib import admin
from edc.base.admin.admin import BaseModelAdmin
from apps.bcpp_household.models import HouseholdStructure
from ..models import RBDEligibility
from apps.bcpp_household_member.models import HouseholdMember
from ..forms import RBDEligibilityForm


class RBDEligibilityAdmin(BaseModelAdmin):

    form = RBDEligibilityForm

    instructions = ['This form is a tool to assist the Interviewer to confirm the Eligibility status of the Research Blood Drwaw subject. After entering the required items, click SAVE. THE DATA WILL BE EVALUATED BUT NOT SAVED.']

    fields = (
        'household_member',
        'dob',
        'part_time_resident',
        'hiv_status')

    radio_fields = {
        "part_time_resident": admin.VERTICAL,
        "hiv_status": admin.VERTICAL, }

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
#         if db_field.name == "household_structure":
#             kwargs["queryset"] = HouseholdStructure.objects.filter(id__exact=request.GET.get('household_structure', 0))
        if db_field.name == "household_member":
            kwargs["queryset"] = HouseholdMember.objects.filter(id__exact=request.GET.get('household_member', 0))
        return super(RBDEligibilityAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(RBDEligibility, RBDEligibilityAdmin)