import factory
from datetime import datetime
from edc.base.model.tests.factories import BaseUuidModelFactory
from ...models import HouseholdLogEntry
from household_log_factory import HouseholdLogFactory


class HouseholdLogEntryFactory(BaseUuidModelFactory):
    FACTORY_FOR = HouseholdLogEntry

    household_log = factory.SubFactory(HouseholdLogFactory)
    report_datetime = datetime.now()
    next_appt_datetime_source = factory.Sequence(lambda n: 'hbc{0}'.format(n))
    household_status = 'eligible_representative_present'