from django.contrib import admin

from edc.base.modeladmin.admin import BaseModelAdmin

from ..forms import RepresentativeEligibilityForm
from ..models import RepresentativeEligibility, HouseholdStructure


class RepresentativeEligibilityAdmin(BaseModelAdmin):

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

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "household_structure":
            kwargs["queryset"] = HouseholdStructure.objects.filter(id__exact=request.GET.get('household_structure', 0))
        return super(RepresentativeEligibilityAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(RepresentativeEligibility, RepresentativeEligibilityAdmin)
