import factory
from datetime import datetime, date
from edc.base.model.tests.factories import BaseUuidModelFactory
from edc.subject.registration.tests.factories import RegisteredSubjectFactory
from ...models import EnrolmentChecklist
from household_member_factory import HouseholdMemberFactory


class EnrolmentChecklistFactory(BaseUuidModelFactory):
    FACTORY_FOR = EnrolmentChecklist

    household_member = factory.SubFactory(HouseholdMemberFactory)
    dob = date(1997,10,10)
    guardian = 'Yes'
    gender = 'M'
    has_identity = 'Yes'
    citizen = 'Yes'
    legal_marriage = 'N/A'
    marriage_certificate = 'N/A'
    part_time_resident = 'Yes'
    household_residency = 'Yes'
    literacy = 'Yes'
