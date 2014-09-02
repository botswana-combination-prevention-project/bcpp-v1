import factory
from edc.base.model.tests.factories import BaseUuidModelFactory
from ...models import PlotLog
from ..factories import PlotFactory


class PlotLogFactory(BaseUuidModelFactory):
    class Meta:
        model = PlotLog

    plot = factory.SubFactory(PlotFactory)
