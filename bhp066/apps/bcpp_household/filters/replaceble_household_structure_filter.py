from django.contrib.admin import SimpleListFilter
from django.utils.translation import ugettext_lazy as _
from django.db.models import Count


class ReplacebleHouseholdStructureFilter(SimpleListFilter):

    title = _('replaceble')

    parameter_name = 'replaceble'

    def queryset(self, request, queryset):
            query_id_list = []
            for household_structure in queryset.all():
                if household_structure.replaceble:
                    query_id_list.append(household_structure.id)
            return queryset.objects.filter(id__in=query_id_list)
