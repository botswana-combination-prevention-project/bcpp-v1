import factory
from bhp_base_model.tests.factories import BaseUuidModelFactory
from bhp_registration.tests.factories import RegisteredSubjectFactory
from bcpp_survey.tests.factories import SurveyFactory
from bcpp_household_member.models import HouseholdMember
from bcpp_household.tests.factories import HouseholdStructureFactory


class HouseholdMemberFactory(BaseUuidModelFactory):
    FACTORY_FOR = HouseholdMember

    household_structure = factory.SubFactory(HouseholdStructureFactory)
    survey = factory.SubFactory(SurveyFactory)
    first_name = factory.Iterator(['ALEX', 'BETSY', 'CHARLIE', 'DODI', 'ERIK', 'FRED', 'GEORGINA', 'HARRIET'])
    initials = factory.Iterator(['AA', 'BB', 'CC', 'DD', 'EE', 'FF', 'GG', 'HH'])
    gender = factory.Iterator(['M', 'F', 'M', 'M', 'M', 'M', 'F', 'F'])
    age_in_years = factory.Iterator([25, 34, 18, 16, 99, 64])
    nights_out = factory.Iterator([0, 1, 3, 15, 17, 12, 3, 0, 0])
