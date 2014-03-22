import factory

from datetime import datetime

from edc.base.model.tests.factories import BaseUuidModelFactory

from apps.bcpp_household_member.tests.factories import HouseholdMemberFactory

from ...models import EnrollmentLoss


class EnrollmentLossFactory(BaseUuidModelFactory):
    FACTORY_FOR = EnrollmentLoss

    household_member = factory.SubFactory(HouseholdMemberFactory)
    report_datetime = datetime.now()
    reason = 'don\'t care'
