import factory
from datetime import date, datetime
from bcpp_subject.tests.factories import SubjectVisitFactory
from base_scheduled_model_factory import BaseScheduledModelFactory
from bcpp_subject.models import AccessToCare


class AccessToCareFactory(BaseScheduledModelFactory):
    FACTORY_FOR = AccessToCare

    subject_visit = factory.SubFactory(SubjectVisitFactory)

    report_datetime = datetime.today()
