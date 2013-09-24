import factory
from datetime import datetime
from bhp_base_test.models import TestVisit
from bhp_visit_tracking.tests.factories import BaseVisitTrackingFactory


class TestVisitFactory(BaseVisitTrackingFactory):
    FACTORY_FOR = TestVisit
