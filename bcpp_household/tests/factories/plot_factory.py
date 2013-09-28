import factory
from edc_lib.bhp_base_model.tests.factories import BaseUuidModelFactory
from bcpp_household.models import Plot


class PlotFactory(BaseUuidModelFactory):
    FACTORY_FOR = Plot

    gps_target_lon = factory.Sequence(lambda n: '2.123{0}'.format(n))
    gps_target_lat = factory.Sequence(lambda n: '2.12345{0}'.format(n))
    community = 'otse'
