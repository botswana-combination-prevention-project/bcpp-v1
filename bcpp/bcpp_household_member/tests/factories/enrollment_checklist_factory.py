import factory

from datetime import datetime, date

from ...models import EnrollmentChecklist

from .household_member_factory import HouseholdMemberFactory


class EnrollmentChecklistFactory(factory.DjangoModelFactory):

    class Meta:
        model = EnrollmentChecklist

    # you need to set these
    household_member = factory.SubFactory(HouseholdMemberFactory)
    dob = date(1997, 10, 10)
    gender = 'M'
    initials = 'NN'
    # these are defaults
    report_datetime = datetime.today()
    has_identity = 'Yes'
    guardian = 'N/A'
    citizen = 'Yes'
    legal_marriage = 'N/A'
    marriage_certificate = 'N/A'
    part_time_resident = 'Yes'
    household_residency = 'Yes'
    literacy = 'Yes'
