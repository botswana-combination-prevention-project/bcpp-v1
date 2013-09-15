from django.contrib import admin
from bcpp_household.models import HouseholdStructure
from bcpp_household.forms import HouseholdStructureForm
from bcpp_household.actions import export_as_kml_hs
from base_household_model_admin import BaseHouseholdModelAdmin


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
        'member_count',
        'note')
    list_display = (
        'plot',
        'survey',
        'house',
        'dashboard',
        'members',
        'logs',
        'progress',
        'member_count',
        'modified',
        'user_modified',
        'hostname_modified')
    list_filter = (
        'survey',
        'progress',
        'member_count',
        'modified',
        'user_modified',
        'hostname_modified',
        )
    search_fields = (
        'plot__plot_identifier',
        'plot__household__household_identifier',
        'plot__household__id', 'id',
        'plot__section',
        'plot__sub_section')
    radio_fields = {
        'survey': admin.VERTICAL,
        }
    readonly_fields = ('survey', )
    list_per_page = 15
admin.site.register(HouseholdStructure, HouseholdStructureAdmin)
