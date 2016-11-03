from django.contrib.admin import SimpleListFilter
from django.utils.translation import ugettext_lazy as _


class ReplacesFilter(SimpleListFilter):

    title = _('replaces')
    parameter_name = 'replaces'

    def lookups(self, request, model_admin):
        return (('Yes', 'Yes'), ('No', 'No'), )

    def queryset(self, request, queryset):
        if self.value() == 'Yes':
            return queryset.filter(replaces__isnull=False)
        if self.value() == 'No':
            return queryset.filter(replaces__isnull=True)
