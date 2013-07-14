import factory
from datetime import date, datetime
from bcpp_subject.tests.factories import SubjectVisitFactory
from base_scheduled_model_factory import BaseScheduledModelFactory
from bcpp_subject.models import StigmaOpinion


class StigmaOpinionFactory(BaseScheduledModelFactory):
    FACTORY_FOR = StigmaOpinion

    subject_visit = factory.SubFactory(SubjectVisitFactory)

    report_datetime = datetime.today()
    test_community_stigma = (('Strongly disagree', 'Strongly disagree'), ('Disagree', 'Disagree'), ('Uncertain', 'Uncertain'), ('Agree', 'Agree'), ('Strongly agree', 'Strongly agree'), ("Don't want to answer", "Don't want to answer"))[0][0]
    gossip_community_stigma = (('Strongly disagree', 'Strongly disagree'), ('Disagree', 'Disagree'), ('Uncertain', 'Uncertain'), ('Agree', 'Agree'), ('Strongly agree', 'Strongly agree'), ("Don't want to answer", "Don't want to answer"))[0][0]
    respect_community_stigma = (('Strongly disagree', 'Strongly disagree'), ('Disagree', 'Disagree'), ('Uncertain', 'Uncertain'), ('Agree', 'Agree'), ('Strongly agree', 'Strongly agree'), ("Don't want to answer", "Don't want to answer"))[0][0]
    enacted_verbal_stigma = (('Strongly disagree', 'Strongly disagree'), ('Disagree', 'Disagree'), ('Uncertain', 'Uncertain'), ('Agree', 'Agree'), ('Strongly agree', 'Strongly agree'), ("Don't want to answer", "Don't want to answer"))[0][0]
    enacted_phyical_stigma = (('Strongly disagree', 'Strongly disagree'), ('Disagree', 'Disagree'), ('Uncertain', 'Uncertain'), ('Agree', 'Agree'), ('Strongly agree', 'Strongly agree'), ("Don't want to answer", "Don't want to answer"))[0][0]
    enacted_family_stigma = (('Strongly disagree', 'Strongly disagree'), ('Disagree', 'Disagree'), ('Uncertain', 'Uncertain'), ('Agree', 'Agree'), ('Strongly agree', 'Strongly agree'), ("Don't want to answer", "Don't want to answer"))[0][0]
    fear_stigma = (('Strongly disagree', 'Strongly disagree'), ('Disagree', 'Disagree'), ('Uncertain', 'Uncertain'), ('Agree', 'Agree'), ('Strongly agree', 'Strongly agree'), ("Don't want to answer", "Don't want to answer"))[0][0]
