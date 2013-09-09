import factory
from lab_result_item.tests.factories import BaseResultItemFactory
from lab_clinic_api.models import ResultItem
from result_factory import ResultFactory
from test_code_factory import TestCodeFactory


class ResultItemFactory(BaseResultItemFactory):
    FACTORY_FOR = ResultItem

    result = factory.SubFactory(ResultFactory)
    test_code = factory.SubFactory(TestCodeFactory)