import factory
from datetime import datetime
from bhp_visit_tracking.models import TestSubjectVisit
from base_visit_tracking_factory import BaseVisitTrackingFactory


class TestSubjectVisitFactory(BaseVisitTrackingFactory):
    FACTORY_FOR = TestSubjectVisit
