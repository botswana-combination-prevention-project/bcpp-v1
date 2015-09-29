from django.contrib import admin

from ..forms import HouseholdRefusalForm
from ..models import HouseholdRefusal

from .base_household_structure_model_admin import BaseHouseholdStructureModelAdmin


class HouseholdRefusalAdmin(BaseHouseholdStructureModelAdmin):

    form = HouseholdRefusalForm
    date_hierarchy = 'modified'
    list_per_page = 30

    fields = (
        'household_structure',
        'report_datetime',
        'reason',
        'reason_other',
        'comment')

    radio_fields = {'reason': admin.VERTICAL}

    list_display = ('household_structure', 'report_datetime', 'created')

    list_filter = ('report_datetime', 'created', 'household_structure__household__community')

    search_fields = ('household_structure__household__household_identifier', 'community', 'id', 'plot__id')

admin.site.register(HouseholdRefusal, HouseholdRefusalAdmin)
