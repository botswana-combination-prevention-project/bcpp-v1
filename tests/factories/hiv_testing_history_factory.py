import factory
from datetime import date, datetime
from bcpp_subject.tests.factories import SubjectVisitFactory
from base_scheduled_model_factory import BaseScheduledModelFactory
from bcpp_subject.models import HivTestingHistory


class HivTestingHistoryFactory(BaseScheduledModelFactory):
    FACTORY_FOR = HivTestingHistory

    subject_visit = factory.SubFactory(SubjectVisitFactory)

    report_datetime = datetime.today()
    has_tested = (('Yes', 'Yes'), ('No', 'No'), ("Don't want to answer", "Don't want to answer"))[0][0]
    other_record = (('Yes', 'Yes'), ('No', 'No'))[0][0]
