import factory

from datetime import datetime

from ...models import SubjectHtc

from .household_member_factory import HouseholdMemberFactory


class SubjectHtcFactory(factory.DjangoModelFactory):

    class Meta:
        model = SubjectHtc

    report_datetime = datetime.today()
    household_member = factory.SubFactory(HouseholdMemberFactory)
    report_datetime = datetime.today()
    offered = 'Yes'
    accepted = 'Yes'
    referred = 'No'
