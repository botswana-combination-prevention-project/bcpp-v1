from datetime import datetime

from ...models import PlotIdentifierHistory

# from .household import HouseholdFactory


class PlotIdentifierHistoryFactory(factory.DjangoModelFactory):
    class Meta:
        model = PlotIdentifierHistory

    # household = factory.SubFactory(HouseholdFactory)
    report_datetime = datetime.now()
    reason = 'Does not have time'
