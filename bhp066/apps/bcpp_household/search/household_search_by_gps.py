from ..forms import GpsSearchForm
from ..models import Household
from .base_search_by_gps import BaseSearchByGps


class HouseholdSearchByGps(BaseSearchByGps):

    name = 'gps'
    search_model = Household
#     search_model_attrname = 'household_identifier'
    order_by = 'household_identifier'
    template = 'search_household_result_include.html'
    search_form = GpsSearchForm
