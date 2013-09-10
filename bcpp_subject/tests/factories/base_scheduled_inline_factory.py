import factory
from datetime import date, datetime
from subject_visit_factory import SubjectVisitFactory
from bcpp_subject.models import BaseScheduledInlineModel
from bhp_base_model.tests.factories import BaseUuidModelFactory

class BaseScheduledInlineModelFactory(BaseUuidModelFactory):
    FACTORY_FOR = BaseScheduledInlineModel
    
    subject_visit = factory.SubFactory(SubjectVisitFactory)
    report_datetime = datetime.today()