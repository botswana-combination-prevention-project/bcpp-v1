import factory

from datetime import datetime

from ...models import PositiveParticipant


class PositiveParticipantFactory(factory.DjangoModelFactory):
    FACTORY_FOR = PositiveParticipant

    report_datetime = datetime.today()
    internalize_stigma = (('Strongly disagree', u'Strongly disagree'), ('Disagree', u'Disagree'), ('Uncertain', u'Uncertain'), ('Agree', u'Agree'), ('Strongly agree', u'Strongly agree'), ('not_answering', u"Don't want to answer"))[0][0]
    internalized_stigma = (('Strongly disagree', u'Strongly disagree'), ('Disagree', u'Disagree'), ('Uncertain', u'Uncertain'), ('Agree', u'Agree'), ('Strongly agree', u'Strongly agree'), ('not_answering', u"Don't want to answer"))[0][0]
    friend_stigma = (('Strongly disagree', u'Strongly disagree'), ('Disagree', u'Disagree'), ('Uncertain', u'Uncertain'), ('Agree', u'Agree'), ('Strongly agree', u'Strongly agree'), ('not_answering', u"Don't want to answer"))[0][0]
    family_stigma = (('Strongly disagree', u'Strongly disagree'), ('Disagree', u'Disagree'), ('Uncertain', u'Uncertain'), ('Agree', u'Agree'), ('Strongly agree', u'Strongly agree'), ('not_answering', u"Don't want to answer"))[0][0]
    enacted_talk_stigma = (('Strongly disagree', u'Strongly disagree'), ('Disagree', u'Disagree'), ('Uncertain', u'Uncertain'), ('Agree', u'Agree'), ('Strongly agree', u'Strongly agree'), ('not_answering', u"Don't want to answer"))[0][0]
    enacted_respect_stigma = (('Strongly disagree', u'Strongly disagree'), ('Disagree', u'Disagree'), ('Uncertain', u'Uncertain'), ('Agree', u'Agree'), ('Strongly agree', u'Strongly agree'), ('not_answering', u"Don't want to answer"))[0][0]
    enacted_jobs_tigma = (('Strongly disagree', u'Strongly disagree'), ('Disagree', u'Disagree'), ('Uncertain', u'Uncertain'), ('Agree', u'Agree'), ('Strongly agree', u'Strongly agree'), ('not_answering', u"Don't want to answer"))[0][0]
