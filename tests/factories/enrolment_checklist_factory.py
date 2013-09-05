import factory
from datetime import date, datetime
from bhp_base_model.tests.factories import BaseUuidModelFactory
from bcpp_household_member.models import EnrolmentChecklist
from bcpp_household_member.tests.factories import HouseholdMemberFactory
from bhp_registration.tests.factories import RegisteredSubjectFactory



class EnrolmentChecklistFactory(BaseUuidModelFactory):
    FACTORY_FOR = EnrolmentChecklist

    household_member = factory.SubFactory(HouseholdMemberFactory)
    registered_subject = factory.SubFactory(RegisteredSubjectFactory)
    report_datetime = datetime.today()
    omang = factory.Sequence(lambda n: 'identity{0}'.format(n))
    citizen = (('Yes', 'Yes'), ('No', 'No'))[0][0]
    community_resident = (('Yes', 'Yes'), ('No', 'No'), ('REF', 'Refused to answer'))[0][0]
