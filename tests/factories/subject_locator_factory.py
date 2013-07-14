import factory
from datetime import date, datetime
from bcpp_subject.tests.factories import SubjectVisitFactory
from base_scheduled_model_factory import BaseScheduledModelFactory
from bcpp_subject.models import SubjectLocator


class SubjectLocatorFactory(BaseScheduledModelFactory):
    FACTORY_FOR = SubjectLocator

    subject_visit = factory.SubFactory(SubjectVisitFactory)

    report_datetime = datetime.today()
    date_signed = date.today()
    home_visit_permission = (('Yes', 'Yes'), ('No', 'No'))[0][0]
    may_follow_up = (('Yes', 'Yes'), ('No', 'No'))[0][0]
    may_call_work = (('Yes', 'Yes'), ('No', 'No'), ('Doesnt_work', 'Doesnt Work'))[0][0]
    may_contact_someone = (('Yes', 'Yes'), ('No', 'No'))[0][0]
    has_alt_contact = (('Yes', 'Yes'), ('No', 'No'))[0][0]
