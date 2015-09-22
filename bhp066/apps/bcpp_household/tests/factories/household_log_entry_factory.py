import factory

from datetime import datetime

from ...models import HouseholdLogEntry

from .household_log_factory import HouseholdLogFactory


class HouseholdLogEntryFactory(factory.DjangoModelFactory):
    class Meta:
        model = HouseholdLogEntry

    household_log = factory.SubFactory(HouseholdLogFactory)
    report_datetime = datetime.now()
    next_appt_datetime_source = factory.Sequence(lambda n: 'hbc{0}'.format(n))
