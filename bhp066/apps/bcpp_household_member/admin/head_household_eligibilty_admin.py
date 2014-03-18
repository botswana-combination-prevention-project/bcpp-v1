from django.contrib import admin
from edc.base.admin.admin import BaseModelAdmin
from apps.bcpp_household.models import HouseholdStructure
from ..models import HouseholdHeadEligibility, HouseholdMember
from ..forms import HouseholdHeadEligibilityForm


class HouseholdHeadEligibilityAdmin(BaseModelAdmin):

    form = HouseholdHeadEligibilityForm
    fields = (
        "household_structure",
        "household_member",
        "report_datetime",
        "aged_over_18",
        "verbal_script",
        )
    radio_fields = {
        "aged_over_18": admin.VERTICAL,
        "verbal_script": admin.VERTICAL,
        }

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "household_member":
            household_members = HouseholdMember.objects.none()
            if HouseholdMember.objects.filter(household_structure__exact=request.GET.get('household_structure', 0), eligible_hoh=None).exists():
                household_members = HouseholdMember.objects.filter(household_structure__exact=request.GET.get('household_structure', 0), eligible_hoh=None)
            kwargs["queryset"] = household_members
        if db_field.name == "household_structure":
            kwargs["queryset"] = HouseholdStructure.objects.filter(id__exact=request.GET.get('household_structure', 0))
        return super(HouseholdHeadEligibilityAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(HouseholdHeadEligibility, HouseholdHeadEligibilityAdmin)
