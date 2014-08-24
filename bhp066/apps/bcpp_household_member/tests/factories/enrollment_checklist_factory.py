import factory

from datetime import date

from edc.base.model.tests.factories import BaseUuidModelFactory

from ...models import EnrollmentChecklist

from .household_member_factory import HouseholdMemberFactory


class EnrollmentChecklistFactory(BaseUuidModelFactory):

    class Meta:
        model = EnrollmentChecklist

    # you need to set these
    household_member = factory.SubFactory(HouseholdMemberFactory)
    dob = date(1997, 10, 10)
    gender = 'M'
    initials = 'NN'
    # these are defaults
    has_identity = 'Yes'
    guardian = 'N/A'
    citizen = 'Yes'
    legal_marriage = 'N/A'
    marriage_certificate = 'N/A'
    part_time_resident = 'Yes'
    household_residency = 'Yes'
    literacy = 'Yes'
