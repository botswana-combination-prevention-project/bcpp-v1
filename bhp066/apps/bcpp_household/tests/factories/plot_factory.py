import factory
from edc.base.model.tests.factories import BaseUuidModelFactory
from ...models import Plot


class PlotFactory(BaseUuidModelFactory):
    FACTORY_FOR = Plot
    
    community = 'otse'
    gps_target_lon = 25.745569 # factory.Sequence(lambda n: '2.123{0}'.format(n))
    gps_target_lat = -25.032927  # factory.Sequence(lambda n: '2.12345{0}'.format(n))
