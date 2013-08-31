from datetime import datetime
from bhp_base_model.tests.factories import BaseUuidModelFactory
from bhp_base_test.models import TestSubjectResultModel


class TestSubjectResultModelFactory(BaseUuidModelFactory):
    FACTORY_FOR = TestSubjectResultModel

    result_datetime = datetime.today()
