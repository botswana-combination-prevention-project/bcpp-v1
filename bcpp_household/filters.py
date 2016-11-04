from django.apps import apps as django_apps
from django.contrib.admin import SimpleListFilter

from edc_constants.constants import YES, NO

from .constants import CONFIRMED, UNCONFIRMED
from .models import Household


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


