import factory
from edc.base.model.tests.factories import BaseUuidModelFactory

from ...models import HouseholdRefusal

from .household_structure_factory import HouseholdStructureFactory


class HouseholdRefusalFactory(BaseUuidModelFactory):
    FACTORY_FOR = HouseholdRefusal

    household_structure = factory.SubFactory(HouseholdStructureFactory)
    reason = 'not_interested'
