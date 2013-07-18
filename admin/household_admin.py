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
        'gps_waypoint',
        'gps_datetime',
        'gps_degrees_s',
        'gps_minutes_s',
        'gps_degrees_e',
        'gps_minutes_e',
        'was_surveyed_previously',
        'cso_number',
        'community',
        'section',
        'sub_section',
        'comment')

    radio_fields = {
        'was_surveyed_previously': admin.VERTICAL, }

    list_display = ('household_identifier', 'cso_number', 'community', 'section', 'created')

    list_filter = ('was_surveyed_previously', 'created', 'target', 'community', 'section',)

    search_fields = ('household_identifier', 'cso_number', 'community', 'section', 'id')

    readonly_fields = ('household_identifier',)

    actions = [process_dispatch, ]

admin.site.register(Household, HouseholdAdmin)
