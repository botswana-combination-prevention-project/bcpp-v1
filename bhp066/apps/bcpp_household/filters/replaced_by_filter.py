from django.contrib.admin import SimpleListFilter
from django.utils.translation import ugettext_lazy as _


class ReplacedByFilter(SimpleListFilter):

    title = _('replaced_by')
    parameter_name = 'replaced_by'

    def lookups(self, request, model_admin):
        return (('Yes', 'Yes'), ('No', 'No'), )

    def queryset(self, request, queryset):
        if self.value() == 'Yes':
            return queryset.filter(replaced_by__isnull=False)
        if self.value() == 'No':
            return queryset.filter(replaced_by__isnull=True)
