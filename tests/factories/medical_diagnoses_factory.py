import factory
from datetime import date, datetime
from bcpp_subject.tests.factories import SubjectVisitFactory
from base_scheduled_model_factory import BaseScheduledModelFactory
from bcpp_subject.models import MedicalDiagnoses


class MedicalDiagnosesFactory(BaseScheduledModelFactory):
    FACTORY_FOR = MedicalDiagnoses

    subject_visit = factory.SubFactory(SubjectVisitFactory)

    report_datetime = datetime.today()
    sti = (('Yes', 'Yes'), ('No', 'No'), ('not sure', 'I am not sure'), ("Don't want to answer", "Don't want to answer"))[0][0]
