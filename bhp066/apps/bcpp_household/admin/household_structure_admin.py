from django.contrib import admin
from apps.bcpp_household.models import HouseholdStructure
from apps.bcpp_household.forms import HouseholdStructureForm
from apps.bcpp_household.actions import export_as_kml_hs
from apps.bcpp_household.filters import ReplaceableHouseholdStructureFilter
from .base_household_model_admin import BaseHouseholdModelAdmin


class HouseholdStructureAdmin(BaseHouseholdModelAdmin):

    def __init__(self, *args, **kwargs):
        self.actions.append(export_as_kml_hs)
        super(HouseholdStructureAdmin, self).__init__(*args, **kwargs)

    form = HouseholdStructureForm
    date_hierarchy = 'modified'

#     def formfield_for_foreignkey(self, db_field, request, **kwargs):
#         if db_field.name == "plot":
#             kwargs["queryset"] = Plot.objects.filter(id__exact=request.GET.get('plot', 0))
#         return super(HouseholdStructureAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    fields = (
        'survey',
        'note')
    list_display = (
        'plot',
        'survey',
        'house',
        'enrolled',
        'refused_enumeration',
        'dashboard',
        'members',
        'logs',
        'progress',
        'modified',
        'user_modified',
        'failed_enumeration_attempts')
    list_filter = (
        'survey',
        'progress',
        'enrolled',
        'refused_enumeration',
        ReplaceableHouseholdStructureFilter,
        'enrolled_datetime',
        'modified',
        'user_modified',
        'hostname_modified',
        'failed_enumeration_attempts',
        )
    search_fields = (
        'household__household_identifier',
        'household__id',
        'id',)
    radio_fields = {
        'survey': admin.VERTICAL,
        }
    readonly_fields = ('survey', )
    list_per_page = 15
admin.site.register(HouseholdStructure, HouseholdStructureAdmin)
