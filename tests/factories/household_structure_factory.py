import factory
from bhp_base_model.tests.factories import BaseUuidModelFactory
from bcpp_survey.tests.factories import SurveyFactory
from bcpp_household.models import HouseholdStructure
from household_factory import HouseholdFactory


class HouseholdStructureFactory(BaseUuidModelFactory):
    FACTORY_FOR = HouseholdStructure

    household = factory.SubFactory(HouseholdFactory)
    survey = factory.SubFactory(SurveyFactory)
    member_count = factory.Iterator([1, 3, 5, 7, 2, 3])
