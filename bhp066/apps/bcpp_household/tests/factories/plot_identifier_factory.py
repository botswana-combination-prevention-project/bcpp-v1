import factory
from datetime import datetime
from edc.base.model.tests.factories import BaseUuidModelFactory
from ...models import PlotIdentifierHistory
from .plot_factory import PlotFactory


class PlotIdentifierHistoryFactory(BaseUuidModelFactory):
    FACTORY_FOR = PlotIdentifierHistory

    household = factory.SubFactory(PlotFactory)
    report_datetime = datetime.now()
    reason = 'Does not have time'