from django.contrib.admin import SimpleListFilter
from django.utils.translation import ugettext_lazy as _

from edc.device.dispatch.models import DispatchItemRegister

from ..models import Plot


class DispatchedReplacesFilter(SimpleListFilter):

    title = _('Replacement plot')
    parameter_name = 'replacement_plot'

    @property
    def plot_pks(self):
        plot_pks = []
        for plot in Plot.objects.filter(replaces__isnull=False):
            try:
                DispatchItemRegister.objects.using('default').get(item_pk=plot.pk)
                plot_pks.append(plot.pk)
            except DispatchItemRegister.DoesNotExist:
                pass
        return plot_pks

    def lookups(self, request, model_admin):
        return (('Yes', 'Dispatched'), ('No', 'Not dispatched'), )

    def queryset(self, request, queryset):
        if self.value() == 'Yes':
            return queryset.filter(pk__in=self.plot_pks, replaces__isnull=False)
        if self.value() == 'No':
            return queryset.filter(replaces__isnull=False).exclude(pk__in=self.plot_pks)
