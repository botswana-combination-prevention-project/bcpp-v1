import factory

from bhp066.apps.bcpp_household.models import PlotLog

from .plot_factory import PlotFactory


class PlotLogFactory(factory.DjangoModelFactory):
    class Meta:
        model = PlotLog

    plot = factory.SubFactory(PlotFactory)
