from django.contrib.admin import SimpleListFilter
from django.utils.translation import ugettext_lazy as _

from ..constants import CONFIRMED, UNCONFIRMED


class ActionFilter(SimpleListFilter):

    title = _('action')
    parameter_name = 'action'

    def lookups(self, request, model_admin):
        return ((CONFIRMED, CONFIRMED), (UNCONFIRMED, UNCONFIRMED), )

    def queryset(self, request, queryset):
        if self.value() == CONFIRMED:
            return queryset.filter(plot__action=CONFIRMED)
        if self.value() == UNCONFIRMED:
            return queryset.filter(plot__action=UNCONFIRMED)
