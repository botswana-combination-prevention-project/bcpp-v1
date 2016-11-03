import factory

from datetime import datetime

from bhp066.apps.bcpp_household.models import PlotIdentifierHistory


class PlotIdentifierHistoryFactory(factory.DjangoModelFactory):
    class Meta:
        model = PlotIdentifierHistory

    # household = factory.SubFactory(HouseholdFactory)
    report_datetime = datetime.now()
    reason = 'Does not have time'
