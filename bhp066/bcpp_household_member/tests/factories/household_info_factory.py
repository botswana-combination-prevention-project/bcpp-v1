import factory
from datetime import datetime
from edc.base.model.tests.factories import BaseUuidModelFactory
from edc.subject.registration.tests.factories import RegisteredSubjectFactory
from bcpp_household_member.models import HouseholdInfo
from bcpp_household.tests.factories import HouseholdStructureFactory
from household_member_factory import HouseholdMemberFactory


class HouseholdInfoFactory(BaseUuidModelFactory):
    FACTORY_FOR = HouseholdInfo

    household_member = factory.SubFactory(HouseholdMemberFactory)
    registered_subject = factory.SubFactory(RegisteredSubjectFactory)
    household_structure = factory.SubFactory(HouseholdStructureFactory)
    report_datetime = datetime.today()
