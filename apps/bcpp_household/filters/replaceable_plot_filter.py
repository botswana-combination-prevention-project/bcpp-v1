from django.contrib.admin import SimpleListFilter
from django.utils.translation import ugettext_lazy as _

from ..helpers.replacement_helper import ReplacementHelper


class ReplaceablePlotFilter(SimpleListFilter):

    title = _('replaceable_calc')
    parameter_name = 'replaceable_calc'

    def lookups(self, request, model_admin):
        return ((True, 'Yes'), (False, 'No'), )

    def queryset(self, request, queryset):
        if self.value():
            query_id_list = []
            for plot in queryset.all():
                replacement_helper = ReplacementHelper(plot=plot)
                if replacement_helper.replaceable_plot:
                    query_id_list.append(plot.id)
                    plot.replaceable = True
                    plot.save_base(update_fields='replaceable')
            return queryset.filter(id__in=query_id_list)
