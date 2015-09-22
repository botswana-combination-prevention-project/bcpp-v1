import factory

from ...models import HouseholdAssessment

from .household_structure_factory import HouseholdStructureFactory


class HouseholdAssessmentFactory(factory.DjangoModelFactory):
    class Meta:
        model = HouseholdAssessment

    household_structure = factory.SubFactory(HouseholdStructureFactory)
