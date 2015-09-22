import factory

from datetime import datetime

from ...models import StigmaOpinion


class StigmaOpinionFactory(factory.DjangoModelFactory):
    FACTORY_FOR = StigmaOpinion

    report_datetime = datetime.today()
    test_community_stigma = (('Strongly disagree', u'Strongly disagree'), ('Disagree', u'Disagree'), ('Uncertain', u'Uncertain'), ('Agree', u'Agree'), ('Strongly agree', u'Strongly agree'), ('not_answering', u"Don't want to answer"))[0][0]
    gossip_community_stigma = (('Strongly disagree', u'Strongly disagree'), ('Disagree', u'Disagree'), ('Uncertain', u'Uncertain'), ('Agree', u'Agree'), ('Strongly agree', u'Strongly agree'), ('not_answering', u"Don't want to answer"))[0][0]
    respect_community_stigma = (('Strongly disagree', u'Strongly disagree'), ('Disagree', u'Disagree'), ('Uncertain', u'Uncertain'), ('Agree', u'Agree'), ('Strongly agree', u'Strongly agree'), ('not_answering', u"Don't want to answer"))[0][0]
    enacted_verbal_stigma = (('Strongly disagree', u'Strongly disagree'), ('Disagree', u'Disagree'), ('Uncertain', u'Uncertain'), ('Agree', u'Agree'), ('Strongly agree', u'Strongly agree'), ('not_answering', u"Don't want to answer"))[0][0]
    enacted_phyical_stigma = (('Strongly disagree', u'Strongly disagree'), ('Disagree', u'Disagree'), ('Uncertain', u'Uncertain'), ('Agree', u'Agree'), ('Strongly agree', u'Strongly agree'), ('not_answering', u"Don't want to answer"))[0][0]
    enacted_family_stigma = (('Strongly disagree', u'Strongly disagree'), ('Disagree', u'Disagree'), ('Uncertain', u'Uncertain'), ('Agree', u'Agree'), ('Strongly agree', u'Strongly agree'), ('not_answering', u"Don't want to answer"))[0][0]
    fear_stigma = (('Strongly disagree', u'Strongly disagree'), ('Disagree', u'Disagree'), ('Uncertain', u'Uncertain'), ('Agree', u'Agree'), ('Strongly agree', u'Strongly agree'), ('not_answering', u"Don't want to answer"))[0][0]
