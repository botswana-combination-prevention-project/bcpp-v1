from django.contrib import admin

from ..forms import RepresentativeEligibilityForm
from ..models import RepresentativeEligibility

from .base_household_structure_model_admin import BaseHouseholdStructureModelAdmin


class RepresentativeEligibilityAdmin(BaseHouseholdStructureModelAdmin):

    form = RepresentativeEligibilityForm
    fields = (
        "household_structure",
        "report_datetime",
        "aged_over_18",
        'household_residency',
        "verbal_script",
    )
    radio_fields = {
        "aged_over_18": admin.VERTICAL,
        "household_residency": admin.VERTICAL,
        "verbal_script": admin.VERTICAL,
    }
    list_filter = ('report_datetime', 'household_structure__household__community')

admin.site.register(RepresentativeEligibility, RepresentativeEligibilityAdmin)
