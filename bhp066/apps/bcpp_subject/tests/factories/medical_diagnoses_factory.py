import factory
from datetime import date, datetime
from edc.base.model.tests.factories import BaseUuidModelFactory
from ...models import MedicalDiagnoses


class MedicalDiagnosesFactory(BaseUuidModelFactory):
    FACTORY_FOR = MedicalDiagnoses

    report_datetime = datetime.today()
