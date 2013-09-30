import factory
from datetime import date, datetime
from edc.base.model.tests.factories import BaseUuidModelFactory
from bcpp_subject.models import FutureHivTesting


class FutureHivTestingFactory(BaseUuidModelFactory):
    FACTORY_FOR = FutureHivTesting

    report_datetime = datetime.today()
