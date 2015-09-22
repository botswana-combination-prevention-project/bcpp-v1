import factory

from ...models import HouseholdLog

from .household_structure_factory import HouseholdStructureFactory


class HouseholdLogFactory(factory.DjangoModelFactory):
    class Meta:
        model = HouseholdLog

    household_structure = factory.SubFactory(HouseholdStructureFactory)
