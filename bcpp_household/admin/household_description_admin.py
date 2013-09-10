from django.contrib import admin
from bcpp_household.models import HouseholdDescription
from base_household_model_admin import BaseHouseholdModelAdmin


class HouseholdDescriptionAdmin(BaseHouseholdModelAdmin):
    pass

admin.site.register(HouseholdDescription, HouseholdDescriptionAdmin)