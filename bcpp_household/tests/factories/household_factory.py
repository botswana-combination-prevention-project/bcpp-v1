import factory
from bhp_base_model.tests.factories import BaseUuidModelFactory
from bcpp_household.models import Household
from plot_factory import PlotFactory


class HouseholdFactory(BaseUuidModelFactory):
    FACTORY_FOR = Household

    household_identifier = factory.Sequence(lambda n: 'household_identifier{0}'.format(n))
    plot = factory.SubFactory(PlotFactory)
    hh_int = 2
    hh_seed = 2
    gps_degrees_s = 2
    gps_minutes_s = 2.5
    gps_degrees_e = 2
    gps_minutes_e = 2.5
    gps_target_lon = 2.1234567
    gps_target_lat = 2.1234567
#    community = factory.Sequence(lambda n: 'community{0}'.format(n))
    community = 'otse'
    section = factory.Sequence(lambda n: 'section{0}'.format(n))
    sub_section = factory.Sequence(lambda n: 'sub_section{0}'.format(n))
