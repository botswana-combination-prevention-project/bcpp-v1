import factory
from datetime import datetime
from subject_visit_factory import SubjectVisitFactory
from apps.bcpp_subject.models import BaseScheduledInlineModel
from edc.base.model.tests.factories import BaseUuidModelFactory


class BaseScheduledInlineModelFactory(BaseUuidModelFactory):
    FACTORY_FOR = BaseScheduledInlineModel

    subject_visit = factory.SubFactory(SubjectVisitFactory)
    report_datetime = datetime.today()
