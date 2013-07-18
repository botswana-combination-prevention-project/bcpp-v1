import factory
from datetime import date, datetime
from bhp_base_model.tests.factories import BaseUuidModelFactory
from bcpp_subject.models import MedicalDiagnoses


class MedicalDiagnosesFactory(BaseUuidModelFactory):
    FACTORY_FOR = MedicalDiagnoses

    report_datetime = datetime.today()
