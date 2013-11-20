import factory
from datetime import datetime
from edc.base.model.tests.factories import BaseUuidModelFactory
from edc.subject.registration.tests.factories import RegisteredSubjectFactory
from ...models import EnrolmentChecklist
from household_member_factory import HouseholdMemberFactory


class EnrolmentChecklistFactory(BaseUuidModelFactory):
    FACTORY_FOR = EnrolmentChecklist

    household_member = factory.SubFactory(HouseholdMemberFactory)
    #registered_subject = factory.SubFactory(RegisteredSubjectFactory)
    #report_datetime = datetime.today()
    #omang = factory.Sequence(lambda n: 'identity{0}'.format(n))
    initials = 'NN'
    part_time_resident = (('Yes', 'Yes'), ('No', 'No'))[0][0]
    has_identity = (('Yes', 'Yes'), ('No', 'No'))[0][0]
    citizen = (('Yes', 'Yes'), ('No', 'No'))[0][0]
    #community_resident = (('Yes', 'Yes'), ('No', 'No'), ('REF', 'Refused to answer'))[0][0]
