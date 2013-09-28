import factory
from datetime import datetime
from edc_lib.bhp_base_model.tests.factories import BaseUuidModelFactory
from edc_lib.bhp_registration.tests.factories import RegisteredSubjectFactory
from bcpp_household_member.models import HouseholdInfo
from bcpp_household.tests.factories import HouseholdStructureFactory
from bcpp_household_member.tests.factories import HouseholdMemberFactory


class HouseholdInfoFactory(BaseUuidModelFactory):
    FACTORY_FOR = HouseholdInfo

    household_member = factory.SubFactory(HouseholdMemberFactory)
    registered_subject = factory.SubFactory(RegisteredSubjectFactory)
    household_structure = factory.SubFactory(HouseholdStructureFactory)
    report_datetime = datetime.today()
