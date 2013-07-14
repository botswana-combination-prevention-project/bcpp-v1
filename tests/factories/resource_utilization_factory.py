import factory
from datetime import date, datetime
from bcpp_subject.tests.factories import SubjectVisitFactory
from base_scheduled_model_factory import BaseScheduledModelFactory
from bcpp_subject.models import ResourceUtilization


class ResourceUtilizationFactory(BaseScheduledModelFactory):
    FACTORY_FOR = ResourceUtilization

    subject_visit = factory.SubFactory(SubjectVisitFactory)

    report_datetime = datetime.today()
    out_patient = (('Yes', 'Yes'), ('No', 'No'), ('REF', 'Refused to answer'))[0][0]
    money_spent = 2.5
    medical_cover = (('Yes', 'Yes'), ('No', 'No'), ('REF', 'Refused to answer'))[0][0]
