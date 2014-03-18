import factory
from edc.base.model.tests.factories import BaseUuidModelFactory
from ...models import EnrolmentChecklist
from household_member_factory import HouseholdMemberFactory


class EnrolmentChecklistFactory(BaseUuidModelFactory):
    FACTORY_FOR = EnrolmentChecklist

    # defaults for an eligible subject but user needs to add household_member, dob, gender, initials)
#     household_member = factory.SubFactory(HouseholdMemberFactory)
#     initials = 'NN'
    has_identity = 'Yes'
    citizen = 'Yes'
    part_time_resident = 'Yes'
    household_residency = 'Yes'
    literacy = 'Yes'
