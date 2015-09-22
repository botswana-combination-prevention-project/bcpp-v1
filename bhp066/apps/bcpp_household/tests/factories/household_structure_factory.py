import factory

from bhp066.apps.bcpp_survey.tests.factories import SurveyFactory

from ...models import HouseholdStructure

from .household_factory import HouseholdFactory


class HouseholdStructureFactory(factory.DjangoModelFactory):
    class Meta:
        model = HouseholdStructure

    survey = factory.SubFactory(SurveyFactory)
    household = factory.SubFactory(HouseholdFactory)
    member_count = 2
    note = factory.Sequence(lambda n: 'note{0}'.format(n))
