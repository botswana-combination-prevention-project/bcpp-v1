import factory
from edc.base.model.tests.factories import BaseUuidModelFactory
from ...models import HouseholdLog
from .household_factory import HouseholdFactory


class HouseholdLogFactory(BaseUuidModelFactory):
    FACTORY_FOR = HouseholdLog

    household_structure = factory.SubFactory(HouseholdFactory)
