import factory

from datetime import datetime

from edc.base.model.tests.factories import BaseUuidModelFactory

from apps.bcpp_household_member.tests.factories import HouseholdMemberFactory
from apps.bcpp_household.tests.factories import HouseholdStructureFactory

from ...models import HouseholdHeadEligibility


class HeadHouseholdEligibilityFactory(BaseUuidModelFactory):
    FACTORY_FOR = HouseholdHeadEligibility

    household_structure = factory.SubFactory(HouseholdStructureFactory)
    household_member = factory.SubFactory(HouseholdMemberFactory)
    report_datetime = datetime.now()
    aged_over_18 = 'Yes'
    household_residency = 'Yes'
    verbal_script = 'Yes'
