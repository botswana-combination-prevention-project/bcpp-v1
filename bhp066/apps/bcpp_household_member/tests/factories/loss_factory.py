import factory
from datetime import datetime
from edc.base.model.tests.factories import BaseUuidModelFactory
from apps.bcpp_household_member.tests.factories import HouseholdMemberFactory
from ...models import Loss


class LossFactory(BaseUuidModelFactory):
    FACTORY_FOR = Loss

    household_member = factory.SubFactory(HouseholdMemberFactory)
    report_datetime = datetime.now()
    reason = 'dont care'