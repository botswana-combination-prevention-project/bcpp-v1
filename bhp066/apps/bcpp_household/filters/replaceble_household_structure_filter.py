from django.contrib.admin import SimpleListFilter
from django.utils.translation import ugettext_lazy as _


class ReplacebleHouseholdStructureFilter(SimpleListFilter):

    title = _('replaceble')

    parameter_name = 'replaceble'

    def lookups(self, request, model_admin):
        return ((True, 'Yes'), (False, 'No'), )

    def queryset(self, request, queryset):
        if self.value():
            query_id_list = []
            for household_structure in queryset.all():
                if household_structure.replaceble and not household_structure.household.replaced_by:
                    query_id_list.append(household_structure.id)
            return queryset.filter(id__in=query_id_list)
