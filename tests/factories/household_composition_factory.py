import factory
from datetime import date, datetime
from bcpp_subject.tests.factories import SubjectVisitFactory
from base_scheduled_model_factory import BaseScheduledModelFactory
from bcpp_subject.models import HouseholdComposition


class HouseholdCompositionFactory(BaseScheduledModelFactory):
    FACTORY_FOR = HouseholdComposition

    subject_visit = factory.SubFactory(SubjectVisitFactory)

    report_datetime = datetime.today()
    coordinates = factory.Sequence(lambda n: 'coordinates{0}'.format(n))
    contact = (('Yes', 'Yes'), ('No', 'No'))[0][0]
    phone_number = 1
