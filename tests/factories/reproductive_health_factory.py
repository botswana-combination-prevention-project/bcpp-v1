import factory
from datetime import date, datetime
from bcpp_subject.tests.factories import SubjectVisitFactory
from base_scheduled_model_factory import BaseScheduledModelFactory
from bcpp_subject.models import ReproductiveHealth


class ReproductiveHealthFactory(BaseScheduledModelFactory):
    FACTORY_FOR = ReproductiveHealth

    subject_visit = factory.SubFactory(SubjectVisitFactory)

    report_datetime = datetime.today()
    number_children = 1
    menopause = (('Yes', 'Yes'), ('No', 'No'))[0][0]
