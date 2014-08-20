import factory
from datetime import date, datetime
from edc.base.model.tests.factories import BaseUuidModelFactory
from subject_visit_factory import SubjectVisitFactory
from ...models import MedicalDiagnoses


class MedicalDiagnosesFactory(BaseUuidModelFactory):
    FACTORY_FOR = MedicalDiagnoses

    subject_visit = factory.SubFactory(SubjectVisitFactory)
    report_datetime = datetime.today()
    heart_attack_record = None
    cancer_record = None
    tb_record = None