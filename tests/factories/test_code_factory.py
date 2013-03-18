import factory
from base_test_code_group_factory import BaseTestCodeGroupFactory
from base_test_code_factory import BaseTestCodeFactory
from lab_test_code.models import TestCode, TestCodeGroup


class TestCodeGroupFactory(BaseTestCodeGroupFactory):
    FACTORY_FOR = TestCodeGroup


class TestCodeFactory(BaseTestCodeFactory):
    FACTORY_FOR = TestCode

    test_code_group = factory.SubFactory(TestCodeGroupFactory)
