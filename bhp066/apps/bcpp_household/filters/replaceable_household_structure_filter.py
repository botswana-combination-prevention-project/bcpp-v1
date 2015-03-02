from django.contrib.admin import SimpleListFilter
from django.utils.translation import ugettext_lazy as _

from ..helpers.replacement_helper import ReplacementHelper


class ReplaceableHouseholdStructureFilter(SimpleListFilter):

    title = _('replaceable')
    parameter_name = 'replaceable'

    def lookups(self, request, model_admin):
        return ((True, 'Yes'), (False, 'No'), )

    def queryset(self, request, queryset):
        if self.value():
            query_id_list = []
            for household_structure in queryset.all():
                replacement_helper = ReplacementHelper(household_structure=household_structure)
                if replacement_helper.replaceable_household:
                    query_id_list.append(household_structure.id)
            return queryset.filter(id__in=query_id_list)
