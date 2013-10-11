import factory
from datetime import date, datetime
from edc.base.model.tests.factories import BaseUuidModelFactory
from ...models import Stigma


class StigmaFactory(BaseUuidModelFactory):
    FACTORY_FOR = Stigma

    report_datetime = datetime.today()
    anticipate_stigma = (('Strongly disagree', u'Strongly disagree'), ('Disagree', u'Disagree'), ('Uncertain', u'Uncertain'), ('Agree', u'Agree'), ('Strongly agree', u'Strongly agree'), ('not_answering', u"Don't want to answer"))[0][0]
    enacted_shame_stigma = (('Strongly disagree', u'Strongly disagree'), ('Disagree', u'Disagree'), ('Uncertain', u'Uncertain'), ('Agree', u'Agree'), ('Strongly agree', u'Strongly agree'), ('not_answering', u"Don't want to answer"))[0][0]
    saliva_stigma = (('Strongly disagree', u'Strongly disagree'), ('Disagree', u'Disagree'), ('Uncertain', u'Uncertain'), ('Agree', u'Agree'), ('Strongly agree', u'Strongly agree'), ('not_answering', u"Don't want to answer"))[0][0]
    teacher_stigma = (('Strongly disagree', u'Strongly disagree'), ('Disagree', u'Disagree'), ('Uncertain', u'Uncertain'), ('Agree', u'Agree'), ('Strongly agree', u'Strongly agree'), ('not_answering', u"Don't want to answer"))[0][0]
    children_stigma = (('Strongly disagree', u'Strongly disagree'), ('Disagree', u'Disagree'), ('Uncertain', u'Uncertain'), ('Agree', u'Agree'), ('Strongly agree', u'Strongly agree'), ('not_answering', u"Don't want to answer"))[0][0]
