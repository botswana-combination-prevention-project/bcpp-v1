import factory
from bhp_base_model.tests.factories import BaseUuidModelFactory
from bcpp_household.models import Plot


class PlotFactory(BaseUuidModelFactory):
    FACTORY_FOR = Plot

#     hh_int = 2
#     hh_seed = 2
#     gps_degrees_s = 2
#     gps_minutes_s = 2.5
#     gps_degrees_e = 2
#     gps_minutes_e = 2.5
    gps_target_lon = factory.Sequence(lambda n: '2.123{0}'.format(n))
    gps_target_lat = factory.Sequence(lambda n: '2.12345{0}'.format(n))
    community = 'otse'
#     section = factory.Sequence(lambda n: 'section{0}'.format(n))
#     sub_section = factory.Sequence(lambda n: 'sub_section{0}'.format(n))
