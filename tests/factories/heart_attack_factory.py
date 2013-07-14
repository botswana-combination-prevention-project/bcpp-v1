import factory
from datetime import date, datetime
from bcpp_subject.tests.factories import SubjectVisitFactory
from base_scheduled_model_factory import BaseScheduledModelFactory
from bcpp_subject.models import HeartAttack


class HeartAttackFactory(BaseScheduledModelFactory):
    FACTORY_FOR = HeartAttack

    subject_visit = factory.SubFactory(SubjectVisitFactory)

    report_datetime = datetime.today()
    date_heart_attack = date.today()
