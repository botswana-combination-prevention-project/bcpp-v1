import factory
from datetime import date, datetime
from bcpp_subject.tests.factories import SubjectVisitFactory
from base_scheduled_model_factory import BaseScheduledModelFactory
from bcpp_subject.models import Stigma


class StigmaFactory(BaseScheduledModelFactory):
    FACTORY_FOR = Stigma

    subject_visit = factory.SubFactory(SubjectVisitFactory)

    report_datetime = datetime.today()
    anticipate_stigma = (('Strongly disagree', 'Strongly disagree'), ('Disagree', 'Disagree'), ('Uncertain', 'Uncertain'), ('Agree', 'Agree'), ('Strongly agree', 'Strongly agree'), ("Don't want to answer", "Don't want to answer"))[0][0]
    enacted_shame_stigma = (('Strongly disagree', 'Strongly disagree'), ('Disagree', 'Disagree'), ('Uncertain', 'Uncertain'), ('Agree', 'Agree'), ('Strongly agree', 'Strongly agree'), ("Don't want to answer", "Don't want to answer"))[0][0]
    saliva_stigma = (('Strongly disagree', 'Strongly disagree'), ('Disagree', 'Disagree'), ('Uncertain', 'Uncertain'), ('Agree', 'Agree'), ('Strongly agree', 'Strongly agree'), ("Don't want to answer", "Don't want to answer"))[0][0]
    teacher_stigma = (('Strongly disagree', 'Strongly disagree'), ('Disagree', 'Disagree'), ('Uncertain', 'Uncertain'), ('Agree', 'Agree'), ('Strongly agree', 'Strongly agree'), ("Don't want to answer", "Don't want to answer"))[0][0]
    children_stigma = (('Strongly disagree', 'Strongly disagree'), ('Disagree', 'Disagree'), ('Uncertain', 'Uncertain'), ('Agree', 'Agree'), ('Strongly agree', 'Strongly agree'), ("Don't want to answer", "Don't want to answer"))[0][0]
