import factory

from datetime import datetime

from edc.base.model.tests.factories import BaseUuidModelFactory

from .household_member_factory import HouseholdMemberFactory

from ...models import EnrollmentLoss


class EnrollmentLossFactory(BaseUuidModelFactory):

    class Meta:
        model = EnrollmentLoss

    household_member = factory.SubFactory(HouseholdMemberFactory)
    report_datetime = datetime.now()
    reason = 'don\'t care'
