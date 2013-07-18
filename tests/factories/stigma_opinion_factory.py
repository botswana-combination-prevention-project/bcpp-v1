import factory
from datetime import date, datetime
from bhp_base_model.tests.factories import BaseUuidModelFactory
from bcpp_subject.models import StigmaOpinion


class StigmaOpinionFactory(BaseUuidModelFactory):
    FACTORY_FOR = StigmaOpinion

    report_datetime = datetime.today()
    test_community_stigma = (('Strongly disagree', 'Strongly disagree'), ('Disagree', 'Disagree'), ('Uncertain', 'Uncertain'), ('Agree', 'Agree'), ('Strongly agree', 'Strongly agree'), ("Don't want to answer", "Don't want to answer"))[0][0]
    gossip_community_stigma = (('Strongly disagree', 'Strongly disagree'), ('Disagree', 'Disagree'), ('Uncertain', 'Uncertain'), ('Agree', 'Agree'), ('Strongly agree', 'Strongly agree'), ("Don't want to answer", "Don't want to answer"))[0][0]
    respect_community_stigma = (('Strongly disagree', 'Strongly disagree'), ('Disagree', 'Disagree'), ('Uncertain', 'Uncertain'), ('Agree', 'Agree'), ('Strongly agree', 'Strongly agree'), ("Don't want to answer", "Don't want to answer"))[0][0]
    enacted_verbal_stigma = (('Strongly disagree', 'Strongly disagree'), ('Disagree', 'Disagree'), ('Uncertain', 'Uncertain'), ('Agree', 'Agree'), ('Strongly agree', 'Strongly agree'), ("Don't want to answer", "Don't want to answer"))[0][0]
    enacted_phyical_stigma = (('Strongly disagree', 'Strongly disagree'), ('Disagree', 'Disagree'), ('Uncertain', 'Uncertain'), ('Agree', 'Agree'), ('Strongly agree', 'Strongly agree'), ("Don't want to answer", "Don't want to answer"))[0][0]
    enacted_family_stigma = (('Strongly disagree', 'Strongly disagree'), ('Disagree', 'Disagree'), ('Uncertain', 'Uncertain'), ('Agree', 'Agree'), ('Strongly agree', 'Strongly agree'), ("Don't want to answer", "Don't want to answer"))[0][0]
    fear_stigma = (('Strongly disagree', 'Strongly disagree'), ('Disagree', 'Disagree'), ('Uncertain', 'Uncertain'), ('Agree', 'Agree'), ('Strongly agree', 'Strongly agree'), ("Don't want to answer", "Don't want to answer"))[0][0]
