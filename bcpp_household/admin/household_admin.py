from django.contrib import admin
from bcpp_household.models import Household
from bcpp_household.forms import HouseholdForm
from bcpp_household.actions import process_dispatch
from base_household_model_admin import BaseHouseholdModelAdmin


class HouseholdAdmin(BaseHouseholdModelAdmin):

    form = HouseholdForm
    date_hierarchy = 'modified'
    list_per_page = 30
    list_max_show_all = 1000

    fields = (
        'report_datetime',
        'status',
        'comment')

    list_display = ('household_identifier', 'structure', 'plot', 'action', 'status', 'community', 'created')

    list_filter = ('status', 'created', 'community', 'action')

    search_fields = ('household_identifier', 'community', 'id', 'plot__id')

    readonly_fields = ('household_identifier',)
    radio_fields = {
        'status': admin.VERTICAL,
        }
    #actions = [process_dispatch, ]

admin.site.register(Household, HouseholdAdmin)
