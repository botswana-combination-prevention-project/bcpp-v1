import factory
from datetime import date, datetime
from bhp_base_model.tests.factories import BaseUuidModelFactory
from bcpp_household_member.models import HouseholdInfo
from bcpp_household.tests.factories import HouseholdStructureFactory
from bcpp_household_member.tests.factories import HouseholdMemberFactory
from bhp_registration.tests.factories import RegisteredSubjectFactory



class HouseholdInfoFactory(BaseUuidModelFactory):
    FACTORY_FOR = HouseholdInfo

    household_member = factory.SubFactory(HouseholdMemberFactory)
    registered_subject = factory.SubFactory(RegisteredSubjectFactory)
    household_structure = factory.SubFactory(HouseholdStructureFactory)
    report_datetime = datetime.today()
#     flooring_type =
#     water_source =
#     energy_source = 
#     toilet_facility =
    
