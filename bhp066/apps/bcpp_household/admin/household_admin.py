from django.contrib import admin

from ..actions import update_replaceables
from ..filters import ReplacedByFilter
from ..forms import HouseholdForm
from ..models import Household

from .base_household_model_admin import BaseHouseholdModelAdmin


class HouseholdAdmin(BaseHouseholdModelAdmin):

    form = HouseholdForm
    date_hierarchy = 'modified'
    list_per_page = 30
    list_max_show_all = 1000

    instructions = []

    list_display = ('household_identifier', 'structure', 'plot', 'community',
                    'replaceable', 'replaced_by', 'created', 'modified')

    list_filter = ('created', 'modified', 'community', 'replaceable', ReplacedByFilter, 'hostname_modified')

    search_fields = ('household_identifier', 'community', 'id', 'plot__id', 'replaced_by')

    readonly_fields = ('plot', 'household_identifier', )

    actions = [update_replaceables, ]

admin.site.register(Household, HouseholdAdmin)
