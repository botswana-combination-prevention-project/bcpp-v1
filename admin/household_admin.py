from django.contrib import admin
from bcpp_household.models import Household
from bcpp_household.forms import HouseholdForm
from bcpp_household.actions import process_dispatch
from base_household_model_admin import BaseHouseholdModelAdmin


class HouseholdAdmin(BaseHouseholdModelAdmin):

    form = HouseholdForm
    date_hierarchy = 'modified'
    list_per_page = 15
    list_max_show_all = 1000

    fields = (
        'report_datetime',
        'status',
        'gps_degrees_s',
        'gps_minutes_s',
        'gps_degrees_e',
        'gps_minutes_e',
        'cso_number',
        'community',
        'section',
        'sub_section',
        'comment')

    list_display = ('household_identifier', 'cso_number', 'community', 'section', 'created')

    list_filter = ('created', 'community', 'section',)

    search_fields = ('household_identifier', 'cso_number', 'community', 'section', 'id')

    readonly_fields = ('household_identifier',)
    radio_fields = {
        'status': admin.VERTICAL,
        }
    actions = [process_dispatch, ]

admin.site.register(Household, HouseholdAdmin)
