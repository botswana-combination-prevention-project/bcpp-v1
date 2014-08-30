from datetime import datetime

from edc.base.model.tests.factories import BaseUuidModelFactory

from ...models import PlotIdentifierHistory

# from .household import HouseholdFactory


class PlotIdentifierHistoryFactory(BaseUuidModelFactory):
    class Meta:
        model = PlotIdentifierHistory

    # household = factory.SubFactory(HouseholdFactory)
    report_datetime = datetime.now()
    reason = 'Does not have time'
