import factory
from lab_requisition.tests.factories import BaseRequisitionFactory
from bhp_base_test.models import TestRequisition
from bhp_base_test.tests.factories import TestVisitFactory


class TestRequisitionFactory(BaseRequisitionFactory):
    FACTORY_FOR = TestRequisition

    test_visit = factory.SubFactory(TestVisitFactory)
