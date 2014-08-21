import factory


from edc.base.model.tests.factories import BaseUuidModelFactory

from ...models import SubjectHtc

from .household_member_factory import HouseholdMemberFactory


class SubjectHtcFactory(BaseUuidModelFactory):

    class Meta:
        model = SubjectHtc

    household_member = factory.SubFactory(HouseholdMemberFactory)
    offered = 'Yes'
    accepted = 'Yes'
    referred = 'No'
