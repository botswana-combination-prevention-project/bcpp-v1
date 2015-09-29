import factory

from bhp066.apps.bcpp_household.models import Plot


class PlotFactory(factory.DjangoModelFactory):
    class Meta:
        model = Plot

    # community = 'otse'
    household_count = 1
    # gps_target_lon = 25.745569 # factory.Sequence(lambda n: '2.123{0}'.format(n))
    # gps_target_lat = -25.032927  # factory.Sequence(lambda n: '2.12345{0}'.format(n))
    gps_target_lon = factory.Sequence(lambda n: '2.123{0}'.format(n))
    gps_target_lat = factory.Sequence(lambda n: '2.12345{0}'.format(n))
    # status = 'residential_habitable'
