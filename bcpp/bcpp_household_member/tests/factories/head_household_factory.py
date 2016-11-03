import factory

from datetime import datetime

from bhp066.apps.bcpp_household.tests.factories import HouseholdStructureFactory

from ...models import HouseholdHeadEligibility

from .household_member_factory import HouseholdMemberFactory


class HeadHouseholdEligibilityFactory(factory.DjangoModelFactory):

    class Meta:
        model = HouseholdHeadEligibility

    household_structure = factory.SubFactory(HouseholdStructureFactory)
    household_member = factory.SubFactory(HouseholdMemberFactory)
    report_datetime = datetime.now()
    aged_over_18 = 'Yes'
    household_residency = 'Yes'
    verbal_script = 'Yes'
