from django.contrib import admin
from apps.bcpp_household.models import HouseholdStructure
from apps.bcpp_household.forms import HouseholdStructureForm
from apps.bcpp_household.actions import export_as_kml_hs
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
        'enrolled',
        'enrolled_datetime',
        'modified',
        'user_modified',
        'hostname_modified',
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
