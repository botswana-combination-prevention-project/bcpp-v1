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
        'gps_device',
        'gps_waypoint',
        'gps_datetime',
        'gps_point_1',
        'gps_point_11',
        'gps_point_2',
        'gps_point_21',
        'was_surveyed_previously',
        'cso_number',
        'village',
        'ward',
        'comment')

    radio_fields = {
        'village': admin.VERTICAL,
        'was_surveyed_previously': admin.VERTICAL,}
    
    filter_horizontal = ('ward',)

    list_display = ('household_identifier', 'cso_number', 'village', 'ward_section', 'created')

    list_filter = ('was_surveyed_previously', 'created', 'target', 'ward_section', 'ward')

    search_fields = ('household_identifier', 'cso_number', 'village', 'ward', 'ward_section', 'id')

    readonly_fields = ('household_identifier',)

    actions = [process_dispatch, ]

admin.site.register(Household, HouseholdAdmin)
