import factory
from datetime import datetime
from edc.base.model.tests.factories import BaseUuidModelFactory
from ...models import HouseholdAssessment
from .household_structure_factory import HouseholdStructureFactory


class HouseholdAssessmentFactory(BaseUuidModelFactory):
    FACTORY_FOR = HouseholdAssessment

    household_sturcture = factory.SubFactory(HouseholdStructureFactory)
