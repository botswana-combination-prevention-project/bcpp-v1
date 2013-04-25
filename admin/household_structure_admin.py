from django.contrib import admin
from bcpp_household.models import Household, HouseholdStructure
from bcpp_household.forms import HouseholdStructureForm
from bcpp_household.actions import export_as_kml_hs
from base_household_model_admin import BaseHouseholdModelAdmin


class HouseholdStructureAdmin(BaseHouseholdModelAdmin):

    def __init__(self, *args, **kwargs):
        self.actions.append(export_as_kml_hs)
        super(HouseholdStructureAdmin, self).__init__(*args, **kwargs)

    form = HouseholdStructureForm
    date_hierarchy = 'modified'

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "household":
            kwargs["queryset"] = Household.objects.filter(id__exact=request.GET.get('household', 0))

        return super(HouseholdStructureAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    fields = (
        'household', 
        'survey', 
        'member_count', 
        'note')
    list_display = (
        'household', 
        'survey', 
        'member_count', 
        'created', 
        'hostname_created')
    list_filter = (
        'survey', 
        'member_count', 
        'created', 
        'hostname_created', 
        'household__ward_section', 
        'household__ward')
    search_fields = (
        'household__household_identifier', 
        'household__id', 'id', 
        'household__ward', 
        'household__ward_section')
    #raw_fields = ("household", "survey")
    radio_fields = {
        'survey': admin.VERTICAL,
        }
    list_per_page = 15

admin.site.register(HouseholdStructure, HouseholdStructureAdmin)
