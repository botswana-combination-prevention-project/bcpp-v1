import factory
from datetime import date, datetime
from bcpp_subject.tests.factories import SubjectVisitFactory
from base_scheduled_model_factory import BaseScheduledModelFactory
from bcpp_subject.models import HivResult


class HivResultFactory(BaseScheduledModelFactory):
    FACTORY_FOR = HivResult

    subject_visit = factory.SubFactory(SubjectVisitFactory)

    report_datetime = datetime.today()
    hiv_result = (('POS', 'HIV Positive (Reactive)'), ('NEG', 'HIV Negative (Non-reactive)'), ('IND', 'Indeterminate'), ('Declined', 'Participant declined testing'), ('Not performed', 'Test could not be performed (e.g. supply outage, technical problem)'))[0][0]
