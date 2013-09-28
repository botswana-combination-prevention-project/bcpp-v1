import factory
from datetime import datetime
from edc_lib.bhp_base_model.tests.factories import BaseUuidModelFactory
from edc_lib.bhp_registration.tests.factories import RegisteredSubjectFactory
from bcpp_household_member.models import EnrolmentChecklist
from bcpp_household_member.tests.factories import HouseholdMemberFactory


class EnrolmentChecklistFactory(BaseUuidModelFactory):
    FACTORY_FOR = EnrolmentChecklist

    household_member = factory.SubFactory(HouseholdMemberFactory)
    registered_subject = factory.SubFactory(RegisteredSubjectFactory)
    report_datetime = datetime.today()
    omang = factory.Sequence(lambda n: 'identity{0}'.format(n))
    citizen = (('Yes', 'Yes'), ('No', 'No'))[0][0]
    community_resident = (('Yes', 'Yes'), ('No', 'No'), ('REF', 'Refused to answer'))[0][0]
