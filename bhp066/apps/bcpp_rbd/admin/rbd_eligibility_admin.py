from django.contrib import admin

from edc.base.admin.admin import BaseModelAdmin

from apps.bcpp_household_member.models import HouseholdMember

from ..forms import RBDEligibilityForm
from ..models import RBDEligibility


class RBDEligibilityAdmin(BaseModelAdmin):

    form = RBDEligibilityForm

    instructions = ['This form is a tool to assist the Interviewer to confirm the Eligibility status of the Research Blood Drwaw subject. After entering the required items, click SAVE. THE DATA WILL BE EVALUATED BUT NOT SAVED.']

    fields = (
        'household_member',
        'initials',
        'dob',
        'gender',
        'hiv_status',
        "part_time_resident",
        'has_identity',
        "citizen",
        "legal_marriage",
        "marriage_certificate",
        "literacy",
        "guardian",)

    radio_fields = {
        'has_identity': admin.VERTICAL,
        "gender": admin.VERTICAL,
        "citizen": admin.VERTICAL,
        "hiv_status": admin.VERTICAL,
        "legal_marriage": admin.VERTICAL,
        "marriage_certificate": admin.VERTICAL,
        "part_time_resident": admin.VERTICAL,
        "literacy": admin.VERTICAL,
        "guardian": admin.VERTICAL,}

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "household_member":
            kwargs["queryset"] = HouseholdMember.objects.filter(id__exact=request.GET.get('household_member', 0))
        return super(RBDEligibilityAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(RBDEligibility, RBDEligibilityAdmin)