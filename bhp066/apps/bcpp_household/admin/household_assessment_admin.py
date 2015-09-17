from django.contrib import admin

from ..forms import HouseholdAssessmentForm
from ..models import HouseholdAssessment, HouseholdStructure

from .base_household_model_admin import BaseHouseholdModelAdmin


class HouseholdAssessmentAdmin(BaseHouseholdModelAdmin):

    form = HouseholdAssessmentForm

    fields = (
        'household_structure',
        'potential_eligibles',
        'eligibles_last_seen_home',
    )

    radio_fields = {
        'potential_eligibles': admin.VERTICAL,
        'eligibles_last_seen_home': admin.VERTICAL,
    }

    list_filter = ('household_structure__household__community',)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "household_structure":
            kwargs["queryset"] = HouseholdStructure.objects.filter(id__exact=request.GET.get('household_structure', 0))
        return super(HouseholdAssessmentAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)
admin.site.register(HouseholdAssessment, HouseholdAssessmentAdmin)
