from django.db.models import Q

from edc.dashboard.search.classes import BaseSearchByWord

from ..models import Plot
from .base_search_by_mixin import BaseSearchByMixin


class PlotSearchByWord(BaseSearchByMixin, BaseSearchByWord):

    name = 'word'
    search_model = Plot
    order_by = 'plot_identifier'
    template = 'search_plot_result_include.html'

    def get_qset_by_filter_keyword(self):
        """Returns a qset based on matching keyword.

        If you predefine keywords, the search term will be intercepted and used to select a query instead."""
        qset_filter = Q()
        qset_exclude = Q()
        if self.get_search_term() in ['confirmed', '-confirmed', 'unconfirmed']:
            if self.get_search_term()[0] == '-':
                qset_exclude = Q(action=self.get_search_term()[1:])
            else:
                qset_filter = Q(action=self.get_search_term())
        if self.get_search_term() in ['occupied', '-occupied', 'vacant', 'non-residential']:
            if self.get_search_term()[0] == '-':
                qset_exclude = Q(status=self.get_search_term()[1:])
            else:
                qset_filter = Q(status=self.get_search_term())
        if qset_filter or qset_exclude:
            return (qset_filter, qset_exclude)
        return None
