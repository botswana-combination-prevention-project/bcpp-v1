from django.contrib import admin
from apps.bcpp_household.forms import HouseholdAssessmentForm
from apps.bcpp_household.models import HouseholdAssessment, Household
from .base_household_model_admin import BaseHouseholdModelAdmin


class HouseholdAssessmentAdmin(BaseHouseholdModelAdmin):

    form = HouseholdAssessmentForm

    fields = (
        'household_structure',
        'residency',
        'member_count',
        'eligibles',
        'ineligibble_reason',
        'last_seen_home',
        )

    radio_fields = {
        'residency': admin.VERTICAL,
        'eligibles': admin.VERTICAL,
        'ineligibble_reason': admin.VERTICAL,
        'last_seen_home': admin.VERTICAL,
        }

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "household_structure":
            kwargs["queryset"] = Household.objects.filter(id__exact=request.GET.get('household_structure', 0))
        return super(HouseholdAssessmentAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)
admin.site.register(HouseholdAssessment, HouseholdAssessmentAdmin)
