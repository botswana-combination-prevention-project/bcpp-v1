import factory
from edc_lib.bhp_base_model.tests.factories import BaseUuidModelFactory
from bcpp_household.models import HouseholdStructure
from bcpp_household.tests.factories import HouseholdFactory
from bcpp_survey.tests.factories import SurveyFactory


class HouseholdStructureFactory(BaseUuidModelFactory):
    FACTORY_FOR = HouseholdStructure

    survey = factory.SubFactory(SurveyFactory)
    household = factory.SubFactory(HouseholdFactory)
    member_count = 2
    note = factory.Sequence(lambda n: 'note{0}'.format(n))
