import factory
from lab_test_code.tests.factories import BaseTestCodeFactory
from lab_clinic_api.models import TestCode, TestCodeGroup


class TestCodeFactory(BaseTestCodeFactory):
    FACTORY_FOR = TestCode


class TestCodeGroupFactory(BaseTestCodeFactory):
    FACTORY_FOR = TestCodeGroup
