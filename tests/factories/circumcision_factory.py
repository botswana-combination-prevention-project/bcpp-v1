import factory
from datetime import date, datetime
from bcpp_subject.tests.factories import SubjectVisitFactory
from base_scheduled_model_factory import BaseScheduledModelFactory
from bcpp_subject.models import Circumcision


class CircumcisionFactory(BaseScheduledModelFactory):
    FACTORY_FOR = Circumcision

    subject_visit = factory.SubFactory(SubjectVisitFactory)

    report_datetime = datetime.today()
    circumcised = (('Yes', 'Yes'), ('No', 'No'), ('not sure', 'I am not sure'), ("Don't want to answer", "Don't want to answer"))[0][0]
