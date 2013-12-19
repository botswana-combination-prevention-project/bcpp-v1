from django.contrib import admin
from apps.bcpp_household.forms import PlotForm
from apps.bcpp_household.actions import process_dispatch
from apps.bcpp_household.models import Plot
from .base_household_model_admin import BaseHouseholdModelAdmin


class PlotAdmin(BaseHouseholdModelAdmin):

    form = PlotForm
    date_hierarchy = 'modified'
    list_per_page = 30
    list_max_show_all = 1000

    fields = (
        'status',
        'gps_degrees_s',
        'gps_minutes_s',
        'gps_degrees_e',
        'gps_minutes_e',
        'cso_number',
        'household_count',
        'eligible_members',
        'time_of_week',
        'time_of_day',
        'description')

    list_display = ('plot_identifier', 'action', 'status', 'cso_number', 'community', 'section', 'created')

    list_filter = ('status', 'bhs', 'created', 'community', 'section', 'sub_section', 'selected', 'action', 'time_of_week', 'time_of_day')

    search_fields = ('plot_identifier', 'cso_number', 'community', 'section', 'id')

    readonly_fields = ('plot_identifier',)
    radio_fields = {
        'status': admin.VERTICAL,
        'time_of_week': admin.VERTICAL,
        'time_of_day': admin.VERTICAL,
        }
    actions = [process_dispatch, ]

admin.site.register(Plot, PlotAdmin)
