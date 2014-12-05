from django.db.models import Q

from edc.dashboard.search.classes import BaseSearchByWord

from ..models import Household


class HouseholdSearchByWord(BaseSearchByWord):

    name = 'word'
    search_model = Household
    order_by = ['household_identifier']
    template = 'search_household_result_include.html'

    @property
    def qset(self):
        qset = Q(household_identifier__icontains=self.search_value)
        return qset
