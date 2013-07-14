import factory
from bhp_visit_tracking.tests.factories import BaseVisitTrackingFactory
from bcpp_subject.models import SubjectVisit


class SubjectVisitFactory(BaseVisitTrackingFactory):
    FACTORY_FOR = SubjectVisit
