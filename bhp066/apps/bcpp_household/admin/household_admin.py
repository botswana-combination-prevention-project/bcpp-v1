from django.contrib import admin
from apps.bcpp_household.models import Household
from apps.bcpp_household.forms import HouseholdForm
from .base_household_model_admin import BaseHouseholdModelAdmin


class HouseholdAdmin(BaseHouseholdModelAdmin):

    form = HouseholdForm
    date_hierarchy = 'modified'
    list_per_page = 30
    list_max_show_all = 1000

    fields = (
        'report_datetime',
        'allowed_to_enumerate',
        'reason_not_enumerate',
        'comment')

    radio_fields = {
        "allowed_to_enumerate": admin.VERTICAL,
        }

    list_display = ('household_identifier', 'structure', 'plot', 'community', 'created')

    list_filter = ('created', 'community')

    search_fields = ('household_identifier', 'community', 'id', 'plot__id')

    readonly_fields = ('household_identifier',)
admin.site.register(Household, HouseholdAdmin)
