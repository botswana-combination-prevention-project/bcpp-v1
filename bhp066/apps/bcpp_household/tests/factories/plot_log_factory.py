import factory

from ...models import PlotLog

from ..factories import PlotFactory


class PlotLogFactory(factory.DjangoModelFactory):
    class Meta:
        model = PlotLog

    plot = factory.SubFactory(PlotFactory)
