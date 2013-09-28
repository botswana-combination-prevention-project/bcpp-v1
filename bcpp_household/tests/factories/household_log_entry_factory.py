import factory
from datetime import datetime
from edc_lib.bhp_base_model.tests.factories import BaseUuidModelFactory
from bcpp_household.models import HouseholdLogEntry
from bcpp_household.tests.factories import HouseholdLogFactory


class HouseholdLogEntryFactory(BaseUuidModelFactory):
    FACTORY_FOR = HouseholdLogEntry

    household_log = factory.SubFactory(HouseholdLogFactory)
    report_datetime = datetime.today()
    hbc = factory.Sequence(lambda n: 'hbc{0}'.format(n))
