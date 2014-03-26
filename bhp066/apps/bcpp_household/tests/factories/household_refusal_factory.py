import factory
from edc.base.model.tests.factories import BaseUuidModelFactory

from ...models import HouseholdEnumerationRefusal

from .household_structure_factory import HouseholdStructureFactory


class HouseholdEnumerationRefusalFactory(BaseUuidModelFactory):
    FACTORY_FOR = HouseholdEnumerationRefusal

    household_structure = factory.SubFactory(HouseholdStructureFactory)
    reason = 'not_interested'
