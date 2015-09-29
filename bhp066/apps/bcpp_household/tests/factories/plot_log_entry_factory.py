import factory

from datetime import datetime

from bhp066.apps.bcpp_household.models import PlotLogEntry

from .plot_log_factory import PlotLogFactory


class PlotLogEntryFactory(factory.DjangoModelFactory):
    class Meta:
        model = PlotLogEntry

    plot_log = factory.SubFactory(PlotLogFactory)
    report_datetime = datetime.now()
