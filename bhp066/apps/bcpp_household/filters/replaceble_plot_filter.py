from django.contrib.admin import SimpleListFilter
from django.utils.translation import ugettext_lazy as _


class ReplaceblePlotFilter(SimpleListFilter):

    title = _('replaceble')
    parameter_name = 'replaceble'

    def lookups(self, request, model_admin):
        return ((True, 'Yes'), (False, 'No'), )

    def queryset(self, request, queryset):
        if self.value():
            query_id_list = []
            for plot in queryset.all():
                if plot.replaceble and not plot.replaced_by:
                    query_id_list.append(plot.id)
            return queryset.filter(id__in=query_id_list)
