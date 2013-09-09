from django.db.models import Q
from bhp_search.forms import DateRangeSearchForm
from base_search import BaseSearch


class BaseSearchByDate(BaseSearch):
    """ subclass of BaseSearch specfic to date range search"""

    search_type = 'date'

    def __init__(self, **kwargs):
        super(BaseSearchByDate, self).__init__(**kwargs)
        defaults = {'search_helptext': 'Search by date.'}
        self.search_form = DateRangeSearchForm
        self.context.update(**defaults)

    def prepare_form(self, request, **kwargs):
        super(BaseSearchByDate, self).prepare_form(request, **kwargs)

    def search(self, request, **kwargs):
        model = self.search_model.get(self.search_model_name)
        qset_created = Q(Q(created__gte="{0} 00:00".format(self.context.get('form').cleaned_data.get('date_start'))),
                       Q(created__lte="{0} 23:59".format(self.context.get('form').cleaned_data.get('date_end'))))
        qset_modified = Q(Q(modified__gte="{0} 00:00".format(self.context.get('form').cleaned_data.get('date_start'))),
                        Q(modified__lte="{0} 23:59".format(self.context.get('form').cleaned_data.get('date_end'))))
        search_result = model.objects.filter(qset_created | qset_modified).order_by('-created')
        kwargs.update({'search_result': search_result})
        super(BaseSearchByDate, self).search(request, **kwargs)
