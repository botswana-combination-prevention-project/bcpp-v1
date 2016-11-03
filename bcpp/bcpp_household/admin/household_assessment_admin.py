from django.contrib import admin

from ..forms import HouseholdAssessmentForm
from ..models import HouseholdAssessment

from .base_household_structure_model_admin import BaseHouseholdStructureModelAdmin


class HouseholdAssessmentAdmin(BaseHouseholdStructureModelAdmin):

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

admin.site.register(HouseholdAssessment, HouseholdAssessmentAdmin)
