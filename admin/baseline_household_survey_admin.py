from django.contrib import admin
from subject_visit_model_admin import SubjectVisitModelAdmin
from bcpp_subject.models import BaselineHouseholdSurvey
from bcpp_subject.forms import BaselineHouseholdSurveyForm



# BaselineHouseholdSurvey
class BaselineHouseholdSurveyAdmin(SubjectVisitModelAdmin):

    form = BaselineHouseholdSurveyForm
    fields = (
        "subject_visit",
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
admin.site.register(BaselineHouseholdSurvey, BaselineHouseholdSurveyAdmin)

