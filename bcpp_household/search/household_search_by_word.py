from django.db.models import Q
from django.conf import settings

from edc.dashboard.search.classes import BaseSearchByWord

from ..models import HouseholdStructure


class HouseholdSearchByWord(BaseSearchByWord):

    name = 'word'
    search_model = HouseholdStructure
    order_by = ['household__household_identifier']
    template = 'search_household_result_include.html'

    @property
    def qset(self):
        qset = Q(household__household_identifier__icontains=self.search_value)
        return qset

    def filtered_default_values(self):
        return {'household__plot__community': settings.CURRENT_COMMUNITY}
