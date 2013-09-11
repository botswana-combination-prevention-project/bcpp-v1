from django.contrib import admin
from base_household_model_admin import BaseHouseholdModelAdmin
from bcpp_household.forms import PlotForm
from bcpp_household.actions import process_dispatch
from bcpp_household.models import Plot

class PlotAdmin(BaseHouseholdModelAdmin):
    
    form = PlotForm
    date_hierarchy = 'modified'
    list_per_page = 30
    list_max_show_all = 1000
    
    

    fields = (
        'availability_datetime',
        'eligible_members',
        'description',
        'num_household',
        'status',
        'gps_degrees_s',
        'gps_minutes_s',
        'gps_degrees_e',
        'gps_minutes_e',
        'cso_number',
        'comment')

    list_display = ('plot_identifier', 'action', 'status', 'cso_number', 'community', 'section', 'created')

    list_filter = ('status', 'created', 'community', 'section', 'sub_section', 'action')

    search_fields = ('plot_identifier', 'cso_number', 'community', 'section', 'id')

    readonly_fields = ('plot_identifier',)
    radio_fields = {
        'status': admin.VERTICAL,
        }
    actions = [process_dispatch, ]
    

    
admin.site.register(Plot, PlotAdmin)