import factory
from datetime import date, datetime
from bcpp_subject.tests.factories import SubjectVisitFactory
from base_scheduled_model_factory import BaseScheduledModelFactory
from bcpp_subject.models import SexualBehaviour


class SexualBehaviourFactory(BaseScheduledModelFactory):
    FACTORY_FOR = SexualBehaviour

    subject_visit = factory.SubFactory(SubjectVisitFactory)

    report_datetime = datetime.today()
    ever_sex = (('Yes', 'Yes'), ('No', 'No'), ("Don't want to answer", "Don't want to answer"))[0][0]
