import factory

from datetime import datetime

from edc.base.model.tests.factories import BaseUuidModelFactory

from apps.bcpp_household_member.tests.factories import HouseholdMemberFactory
from apps.bcpp_household.tests.factories import HouseholdStructureFactory

from ...models import SubjectHtc


class SubjectHtcFactory(BaseUuidModelFactory):
    FACTORY_FOR = SubjectHtc

    household_member = factory.SubFactory(HouseholdMemberFactory)
    offered = 'Yes'
    accepted = 'Yes'
    hiv_result = 'NEG'
    referred = 'No'
