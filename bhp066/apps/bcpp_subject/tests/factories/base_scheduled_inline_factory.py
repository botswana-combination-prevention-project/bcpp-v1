import factory
from datetime import datetime
from subject_visit_factory import SubjectVisitFactory
from edc.base.model.tests.factories import BaseUuidModelFactory
from ...models import BaseScheduledInlineModel


class BaseScheduledInlineModelFactory(BaseUuidModelFactory):
    FACTORY_FOR = BaseScheduledInlineModel

    subject_visit = factory.SubFactory(SubjectVisitFactory)
    report_datetime = datetime.today()
