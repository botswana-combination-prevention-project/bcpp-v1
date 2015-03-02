import factory
from edc.base.model.tests.factories import BaseUuidModelFactory
from .subject_visit_factory import SubjectVisitFactory


class BaseScheduledModelFactory(BaseUuidModelFactory):
    ABSTRACT_FACTORY = True

    subject_visit = factory.SubFactory(SubjectVisitFactory)
