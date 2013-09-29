import factory
from datetime import datetime
from edc_core.bhp_base_model.tests.factories import BaseUuidModelFactory
from ...models import HouseholdLogEntry
from household_log_factory import HouseholdLogFactory


class HouseholdLogEntryFactory(BaseUuidModelFactory):
    FACTORY_FOR = HouseholdLogEntry

    household_log = factory.SubFactory(HouseholdLogFactory)
    report_datetime = datetime.today()
    hbc = factory.Sequence(lambda n: 'hbc{0}'.format(n))
