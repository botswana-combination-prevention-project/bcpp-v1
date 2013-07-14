import factory
from datetime import date, datetime
from bcpp_subject.tests.factories import SubjectVisitFactory
from base_scheduled_model_factory import BaseScheduledModelFactory
from bcpp_subject.models import TodaysHivResult


class TodaysHivResultFactory(BaseScheduledModelFactory):
    FACTORY_FOR = TodaysHivResult

    subject_visit = factory.SubFactory(SubjectVisitFactory)

    report_datetime = datetime.today()
    hiv_result = (('Positive', 'Positive'), ('Negative', 'Negative'), ('Indeterminate', 'Indeterminate'), ('Declined', 'Participant declined testing'), ('Not performed', 'Test could not be performed (e.g. supply outage, technical problem)'))[0][0]
