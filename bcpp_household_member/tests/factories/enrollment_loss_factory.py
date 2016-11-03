import factory

from datetime import datetime

from .household_member_factory import HouseholdMemberFactory

from ...models import EnrollmentLoss


class EnrollmentLossFactory(factory.DjangoModelFactory):

    class Meta:
        model = EnrollmentLoss

    household_member = factory.SubFactory(HouseholdMemberFactory)
    report_datetime = datetime.now()
    reason = 'don\'t care'
