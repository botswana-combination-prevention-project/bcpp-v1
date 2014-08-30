import factory

from datetime import datetime

from edc.base.model.tests.factories import BaseUuidModelFactory

from ...models import PlotLogEntry

from .plot_log_factory import PlotLogFactory


class PlotLogEntryFactory(BaseUuidModelFactory):
    class Meta:
        model = PlotLogEntry

    plot_log = factory.SubFactory(PlotLogFactory)
    report_datetime = datetime.now()
