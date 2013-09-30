import factory
from edc.base.model.tests.factories import BaseUuidModelFactory
from bcpp_survey.tests.factories import SurveyFactory
from ...models import HouseholdStructure
from .household_factory import HouseholdFactory


class HouseholdStructureFactory(BaseUuidModelFactory):
    FACTORY_FOR = HouseholdStructure

    survey = factory.SubFactory(SurveyFactory)
    household = factory.SubFactory(HouseholdFactory)
    member_count = 2
    note = factory.Sequence(lambda n: 'note{0}'.format(n))
