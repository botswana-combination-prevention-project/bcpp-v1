import factory

from bhp066.apps.bcpp_household.models import HouseholdLog

from .household_structure_factory import HouseholdStructureFactory


class HouseholdLogFactory(factory.DjangoModelFactory):
    class Meta:
        model = HouseholdLog

    household_structure = factory.SubFactory(HouseholdStructureFactory)
