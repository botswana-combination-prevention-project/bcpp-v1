from django.contrib import admin
from apps.bcpp_household.forms import HouseholdResidencyStatusAssessmentForm
from apps.bcpp_household.actions import process_dispatch
from apps.bcpp_household.models import HouseholdResidencyStatusAssessment, Household
from .base_household_model_admin import BaseHouseholdModelAdmin


class HouseholdResidencyStatusAssessmentAdmin(BaseHouseholdModelAdmin):

    form = HouseholdResidencyStatusAssessmentForm

    fields = (
        'household',
        'residency',
        'member_count',
        'citizen',
        'how_many',
        'possible_eligibles',
        'how_many_members',
        'original_community',
        'original_community_other',
        'last_seen_home',
        'most_likely',
        )

#     list_display = ('household', 'residency', 'member_count', 'citizen', 'how_many', 'original_community',)

    radio_fields = {
        'residency': admin.VERTICAL,
        'citizen': admin.VERTICAL,
        'possible_eligibles': admin.VERTICAL,
        'original_community': admin.VERTICAL,
        'last_seen_home': admin.VERTICAL,
        }
    filter_horizontal = ('most_likely',)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "household":
            kwargs["queryset"] = Household.objects.filter(id__exact=request.GET.get('household', 0))
        return super(HouseholdResidencyStatusAssessmentAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)
admin.site.register(HouseholdResidencyStatusAssessment, HouseholdResidencyStatusAssessmentAdmin)
