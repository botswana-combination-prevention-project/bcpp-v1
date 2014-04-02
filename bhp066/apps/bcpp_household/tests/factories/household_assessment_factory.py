import factory

from edc.base.model.tests.factories import BaseUuidModelFactory

from ...models import HouseholdAssessment

from .household_structure_factory import HouseholdStructureFactory


class HouseholdAssessmentFactory(BaseUuidModelFactory):
    FACTORY_FOR = HouseholdAssessment

    household_structure = factory.SubFactory(HouseholdStructureFactory)