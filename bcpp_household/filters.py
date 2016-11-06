from django.contrib.admin import SimpleListFilter

from .constants import CONFIRMED, UNCONFIRMED


class ActionFilter(SimpleListFilter):

    title = 'action'
    parameter_name = 'action'

    def lookups(self, request, model_admin):
        return ((CONFIRMED, CONFIRMED), (UNCONFIRMED, UNCONFIRMED), )

    def queryset(self, request, queryset):
        if self.value() == CONFIRMED:
            return queryset.filter(plot__action=CONFIRMED)
        if self.value() == UNCONFIRMED:
            return queryset.filter(plot__action=UNCONFIRMED)
