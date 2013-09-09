import factory
from lab_requisition.tests.factories import BaseClinicRequisitionFactory
from bhp_base_test.models import TestRequisition
from bhp_base_test.tests.factories import TestVisitFactory


class TestRequisitionFactory(BaseClinicRequisitionFactory):
    FACTORY_FOR = TestRequisition

    test_visit = factory.SubFactory(TestVisitFactory)
