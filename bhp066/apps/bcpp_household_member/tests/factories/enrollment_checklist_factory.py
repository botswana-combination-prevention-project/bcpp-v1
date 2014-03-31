import factory
from datetime import date
from edc.base.model.tests.factories import BaseUuidModelFactory
from ...models import EnrollmentChecklist
from household_member_factory import HouseholdMemberFactory


class EnrollmentChecklistFactory(BaseUuidModelFactory):
    FACTORY_FOR = EnrollmentChecklist

    household_member = factory.SubFactory(HouseholdMemberFactory)
    dob = date(1997, 10, 10)
    guardian = 'N/A'
    gender = 'M'
    citizen = 'Yes'
    legal_marriage = 'N/A'
    marriage_certificate = 'N/A'
    # defaults for an eligible subject but user needs to add household_member, dob, gender, initials)
    initials = 'NN'
    has_identity = 'Yes'
    part_time_resident = 'Yes'
    household_residency = 'Yes'
    literacy = 'Yes'
