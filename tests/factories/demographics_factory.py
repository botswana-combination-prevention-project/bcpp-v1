import factory
from datetime import date, datetime
from bhp_base_model.tests.factories import BaseUuidModelFactory
from bcpp_subject.models import Demographics


class DemographicsFactory(BaseUuidModelFactory):
    FACTORY_FOR = Demographics

    report_datetime = datetime.today()
    religion_other = factory.Sequence(lambda n: 'religion_other{0}'.format(n))
    ethnic = (('Babirwa', u'Babirwa'), ('Bahambukushu', u'Bahambukushu'), ('Baherero', u'Baherero'), ('Bahurutshe', u'Bahurutshe'), ('Bakalaka', u'Bakalaka'), ('Bakgatla', u'Bakgatla'), ('Bakwena', u'Bakwena'), ('Balete', u'Balete'), ('Bangwaketse', u'Bangwaketse'), ('Bangwato', u'Bangwato'), ('Bakgalagadi', u'Bakgalagadi'), ('Basarwa', u'Basarwa'), ('Basobea', u'Basobea'), ('Batawana', u'Batawana'), ('Batlokwa', u'Batlokwa'), ('Batswapong', u'Batswapong'), ('White African', u'White African'), ('Indian African', u'Indian African'), ('Asian', u'Asian'), ('Other, specify:', u'Other, specify:'), ("Don't want to answer", u"Don't want to answer"))[0][0]
    other = factory.Sequence(lambda n: 'other{0}'.format(n))
    marital_status = (('Single/never married', u'Single/never married'), ('Married', u'Married (common law/civil or customary/traditional)'), ('Divorced/separated', u'Divorced or formally separated'), ('Widowed', u'Widowed'), ("Don't want to answer", u"Don't want to answer"))[0][0]
