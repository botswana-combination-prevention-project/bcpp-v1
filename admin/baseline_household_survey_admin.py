from django.contrib import admin
from django.db.models import get_model
from bhp_base_admin.admin import BaseModelAdmin
from bcpp_household_member.models import BaselineHouseholdSurvey, HouseholdMember
from bcpp_household_member.forms import BaselineHouseholdSurveyForm


# BaselineHouseholdSurvey
class BaselineHouseholdSurveyAdmin(BaseModelAdmin):

    form = BaselineHouseholdSurveyForm
    fields = (
        "household_member",
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

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "household_member":
            household_members = []
            SubjectConsent = get_model('bcpp_subject', 'SubjectConsent')
            for hm in HouseholdMember.objects.filter(household_structure__exact=request.GET.get('household_structure', 0)):
                if SubjectConsent.objects.filter(registered_subject=hm.registered_subject):
                    household_members.append(hm)
            kwargs["queryset"] = household_members

        return super(BaselineHouseholdSurveyAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(BaselineHouseholdSurvey, BaselineHouseholdSurveyAdmin)
