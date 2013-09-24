import factory
from bhp_off_study.tests.factories import BaseOffStudyFactory
from bhp_base_test.models import TestBaseOffStudy


class TestBaseOffStudyFactory(BaseOffStudyFactory):
    FACTORY_FOR = TestBaseOffStudy
