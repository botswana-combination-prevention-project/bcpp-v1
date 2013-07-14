import factory
from datetime import date, datetime
from bhp_base_model.tests.factories import BaseUuidModelFactory
from bhp_registration.tests.factories import RegisteredSubjectFactory
from bcpp_subject.models import EnrolmentChecklist


class EnrolmentChecklistFactory(BaseUuidModelFactory):
    FACTORY_FOR = EnrolmentChecklist

    registered_subject = factory.SubFactory(RegisteredSubjectFactory)
    registration_datetime = datetime.today()
    census_number = factory.Sequence(lambda n: 'census_number{0}'.format(n))
    mental_capacity = (('Yes', 'Yes'), ('No', 'No'))[0][0]
    incarceration = (('Yes', 'Yes'), ('No', 'No'))[1][0]
    citizen = (('Yes', 'Yes'), ('No', 'No'))[0][0]
    community_resident = (('Yes', 'Yes'), ('No', 'No'), ('REF', 'Refused to answer'))[0][0]
