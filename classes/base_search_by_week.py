from django.db.models import Q
from bhp_search.forms import WeekYearSearchForm
from base_search import BaseSearch
from week import Week


class BaseSearchByWeek(BaseSearch):

    search_type = 'week'

    def __init__(self, **kwargs):
        super(BaseSearchByWeek, self).__init__(**kwargs)
        defaults = {'search_helptext': 'Search by date.'}
        self.search_form = WeekYearSearchForm
        self.context.update(**defaults)

    def prepare_form(self, request, **kwargs):
        super(BaseSearchByWeek, self).prepare_form(request, **kwargs)

    def search(self, request, **kwargs):

        model = self.search_model.get(self.search_model_name)
        #this form returns week numbers so convert to datetime
        week = Week()
        wb_start = week.boundaries(self.context.get('form').cleaned_data.get('year_start'), int(self.context.get('form').cleaned_data.get('week_start')))
        wb_end = week.boundaries(self.context.get('form').cleaned_data.get('year_end'), int(self.context.get('form').cleaned_data.get('week_end')))

        qset_created = Q(Q(created__gte="%s 00:00" % (wb_start[0])),
                       Q(created__lte="%s 23:59" % (wb_end[1])))
        qset_modified = Q(Q(modified__gte="%s 00:00" % (wb_start[0])),
                        Q(modified__lte="%s 23:59" % (wb_end[1])))
        search_result = model.objects.filter(qset_created | qset_modified).order_by('-created')
        kwargs.update({'search_result': search_result})
        super(BaseSearchByWeek, self).search(request, **kwargs)
