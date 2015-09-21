from django.contrib import admin

from ..actions import export_as_kml_hs
from ..forms import HouseholdStructureForm
from ..models import HouseholdStructure

from .base_household_model_admin import BaseHouseholdModelAdmin


class HouseholdStructureAdmin(BaseHouseholdModelAdmin):

    def __init__(self, *args, **kwargs):
        self.actions.append(export_as_kml_hs)
        super(HouseholdStructureAdmin, self).__init__(*args, **kwargs)

    form = HouseholdStructureForm
    date_hierarchy = 'modified'
    instructions = []
    # fields = (
    #    'survey',
    #    'note')
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
        'household__community',
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
