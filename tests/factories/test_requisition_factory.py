import factory
from lab_requisition.tests.factories import BaseClinicRequisitionFactory
from lab_requisition.models import TestRequisition
from bhp_visit_tracking.tests.factories import TestSubjectVisitFactory


class TestRequisitionFactory(BaseClinicRequisitionFactory):
    FACTORY_FOR = TestRequisition

    test_subject_visit = factory.SubFactory(TestSubjectVisitFactory)
