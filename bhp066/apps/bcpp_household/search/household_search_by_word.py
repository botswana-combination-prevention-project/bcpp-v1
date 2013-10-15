from django.conf import settings

from edc.dashboard.search.classes import BaseSearchByWord

# from ..section import SectionHouseholdView
from ..models import Household


class HouseholdSearchByWord(BaseSearchByWord):

    search_model = Household
    order_by = 'household_identifier'
    template = 'search_household_result_include.html'

    def get_most_recent_query_options(self):
        return {'plot__community': settings.CURRENT_COMMUNITY}
