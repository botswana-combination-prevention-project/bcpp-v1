import factory
from datetime import date, datetime
from bcpp_subject.tests.factories import SubjectVisitFactory
from base_scheduled_model_factory import BaseScheduledModelFactory
from bcpp_subject.models import Circumcised


class CircumcisedFactory(BaseScheduledModelFactory):
    FACTORY_FOR = Circumcised

    subject_visit = factory.SubFactory(SubjectVisitFactory)

    report_datetime = datetime.today()
