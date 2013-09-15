import factory
from bhp_base_model.tests.factories import BaseUuidModelFactory
from bcpp_household.models import Household
from plot_factory import PlotFactory


class HouseholdFactory(BaseUuidModelFactory):
    FACTORY_FOR = Household

    plot = factory.SubFactory(PlotFactory)
#     gps_degrees_s = 2
#     gps_minutes_s = 2.5
#     gps_degrees_e = 2
#     gps_minutes_e = 2.5
#     gps_target_lon = 2.1234567
#     gps_target_lat = 2.1234567
