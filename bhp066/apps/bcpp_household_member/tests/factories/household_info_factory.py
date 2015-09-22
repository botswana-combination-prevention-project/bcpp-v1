import factory

from datetime import datetime

from edc.subject.registration.tests.factories import RegisteredSubjectFactory

from bhp066.apps.bcpp_household_member.models import HouseholdInfo
from bhp066.apps.bcpp_household.tests.factories import HouseholdStructureFactory

from .household_member_factory import HouseholdMemberFactory


class HouseholdInfoFactory(factory.DjangoModelFactory):

    class Meta:
        model = HouseholdInfo

    household_member = factory.SubFactory(HouseholdMemberFactory)
    registered_subject = factory.SubFactory(RegisteredSubjectFactory)
    household_structure = factory.SubFactory(HouseholdStructureFactory)
    report_datetime = datetime.today()
