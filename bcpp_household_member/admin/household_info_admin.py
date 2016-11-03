from django.contrib import admin

from edc_base.modeladmin.admin import BaseModelAdmin

from bhp066.apps.bcpp_household.models import HouseholdStructure

from ..forms import HouseholdInfoForm
from ..models import HouseholdInfo, HouseholdMember


class HouseholdInfoAdmin(BaseModelAdmin):

    form = HouseholdInfoForm
    fields = (
        "household_structure",
        "household_member",
        "report_datetime",
        "flooring_type",
        "flooring_type_other",
        "living_rooms",
        "water_source",
        "water_source_other",
        "energy_source",
        "energy_source_other",
        "toilet_facility",
        "toilet_facility_other",
        "electrical_appliances",
        "transport_mode",
        "goats_owned",
        "sheep_owned",
        "cattle_owned",
        "smaller_meals",
    )
    radio_fields = {
        "flooring_type": admin.VERTICAL,
        "water_source": admin.VERTICAL,
        "energy_source": admin.VERTICAL,
        "toilet_facility": admin.VERTICAL,
        "smaller_meals": admin.VERTICAL,
    }
    filter_horizontal = (
        "electrical_appliances",
        "transport_mode",
    )
    list_filter = ('report_datetime', 'household_member__household_structure__household__community')

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "household_member":
            kwargs["queryset"] = HouseholdMember.objects.filter(
                household_structure__exact=request.GET.get('household_structure', 0), age_in_years__in=range(18L, 110L))
        if db_field.name == "household_structure":
            kwargs["queryset"] = HouseholdStructure.objects.filter(id__exact=request.GET.get('household_structure', 0))
        return super(HouseholdInfoAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(HouseholdInfo, HouseholdInfoAdmin)
