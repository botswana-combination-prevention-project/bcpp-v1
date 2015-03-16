from edc.export.helpers import ExportObjectHelper
from apps.bcpp_household.models import Household as HouseholdModel

from ..classes import Household

from .base_collector import BaseCollector


class Households(BaseCollector):

    """Exports helper.household instances to CSV.

    For example::
        from apps.bcpp_export.collectors import Households

        households = Households()
        households.export_to_csv()
    """

    def __init__(self, export_plan=None, community=None, exception_cls=None):
        super(Households, self).__init__(export_plan=export_plan, community=community, exception_cls=exception_cls)

    def export_to_csv(self):
        for community in self.community_list:
            print '{} **************************************'.format(community)
            for household in HouseholdModel.objects.filter(plot__community=community).order_by('household_identifier'):
                household = Household(household)
                self._export(household)
                if self.test_run:
                    break
