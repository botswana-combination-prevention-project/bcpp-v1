from django.db.models import Q
from django.conf import settings

from edc.dashboard.search.classes import BaseSearchByWord
from edc.device.device.classes import Device

from ..constants import (CONFIRMED, UNCONFIRMED, RESIDENTIAL_HABITABLE,
                         NON_RESIDENTIAL, RESIDENTIAL_NOT_HABITABLE)
from ..models import Plot


class PlotSearchByWord(BaseSearchByWord):

    name = 'word'
    search_model = Plot
    order_by = ['plot_identifier']
    template = 'search_plot_result_include.html'

    def contribute_to_context(self, context):
        context = super(PlotSearchByWord, self).contribute_to_context(context)
        context.update({'CONFIRMED': CONFIRMED},
                       device=Device())
        return context

    @property
    def qset(self):
        qset = (
            Q(plot_identifier__icontains=self.search_value) |
            Q(description__icontains=self.search_value) |
            Q(cso_number__icontains=self.search_value)
        )
        return qset

    def qset_by_filter_keyword(self):
        """Returns a qset based on matching keyword.

        If you predefine keywords, the search term will be intercepted and used to select a query instead."""
        qset_filter = None
        qset_exclude = None
        if self.search_value in [CONFIRMED, '-{}'.format(CONFIRMED), UNCONFIRMED]:
            if self.search_value[0] == '-':
                qset_exclude = Q(action=self.search_value[1:])
            else:
                qset_filter = Q(action=self.search_value)
        if self.search_value in [RESIDENTIAL_HABITABLE, '-'.format(RESIDENTIAL_HABITABLE),
                                 RESIDENTIAL_NOT_HABITABLE, NON_RESIDENTIAL]:
            if self.search_value[0] == '-':
                qset_exclude = Q(status=self.search_value[1:])
            else:
                qset_filter = Q(status=self.search_value)
        if qset_filter or qset_exclude:
            return (qset_filter, qset_exclude)
        return None

    def filtered_default_values(self):
        return {'community': settings.CURRENT_COMMUNITY}
