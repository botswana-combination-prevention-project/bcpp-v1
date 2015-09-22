import factory

from datetime import datetime

from ...models import MonthsThirdPartner


class MonthsThirdPartnerFactory(factory.DjangoModelFactory):
    FACTORY_FOR = MonthsThirdPartner

    report_datetime = datetime.today()
    third_last_sex = (('Days', u'Days'), ('Months', u'Months'), ('not_answering', u"Don't want to answer"))[0][0]
    third_last_sex_calc = 2
    first_first_sex = (('Days', u'Days'), ('Months', u'Months'), ('Years', u'Years'), ('not_answering', u"Don't want to answer"))[0][0]
    first_first_sex_calc = 2
    first_sex_current = (('Yes', u'Yes'), ('No', u'No'), ('not_answering', u"Don't want to answer"))[0][0]
    first_relationship = (('Long-term partner', u'Long-term partner (>2 years) or spouse'), ('2 years or spouse', u'2 years or spouse'), ('Boyfriend/Girlfriend', u'Boyfriend/Girlfriend'), ('Casual (known) partner', u'Casual (known) partner'), ('One time partner (previously unknown)', u'One time partner (previously unknown)'), ('Commercial sex worker', u'Commercial sex worker'), ('OTHER', u'Other, specify:'), ('not_answering', u"Don't want to answer"))[0][0]
    concurrent = (('Yes', u'Yes'), ('No', u'No'), ('not_answering', u"Don't want to answer"))[0][0]
    goods_exchange = (('Yes', u'Yes'), ('No', u'No'), ('not_answering', u"Don't want to answer"))[0][0]
    first_sex_freq = 2
    partner_hiv_test = (('Yes', u'Yes'), ('No', u'No'), ('not_sure', u'I am not sure'), ('not_answering', u"Don't want to answer"))[0][0]
