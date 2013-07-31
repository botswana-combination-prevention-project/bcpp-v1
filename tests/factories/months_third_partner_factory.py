import factory
from datetime import date, datetime
from bhp_base_model.tests.factories import BaseUuidModelFactory
from bcpp_subject.models import MonthsThirdPartner


class MonthsThirdPartnerFactory(BaseUuidModelFactory):
    FACTORY_FOR = MonthsThirdPartner

    report_datetime = datetime.today()
    third_last_sex = (('Days', u'Days'), ('Months', u'Months'), ("Don't want to answer", u"Don't want to answer"))[0][0]
    third_last_sex_calc = 2
    first_first_sex = (('Days', u'Days'), ('Months', u'Months'), ('Years', u'Years'), ("Don't want to answer", u"Don't want to answer"))[0][0]
    first_first_sex_calc = 2
    first_sex_current = (('Yes', u'Yes'), ('No', u'No'), ("Don't want to answer", u"Don't want to answer"))[0][0]
    first_relationship = (('Long-term partner', u'Long-term partner (>2 years) or spouse'), ('2 years or spouse', u'2 years or spouse'), ('Boyfriend/Girlfriend', u'Boyfriend/Girlfriend'), ('Casual (known) partner', u'Casual (known) partner'), ('One time partner (previously unknown)', u'One time partner (previously unknown)'), ('Commercial sex worker', u'Commercial sex worker'), ('Other, specify:', u'Other, specify:'), ("Don't want to answer", u"Don't want to answer"))[0][0]
    concurrent = (('Yes', u'Yes'), ('No', u'No'), ("Don't want to answer", u"Don't want to answer"))[0][0]
    goods_exchange = (('Yes', u'Yes'), ('No', u'No'), ("Don't want to answer", u"Don't want to answer"))[0][0]
    first_sex_freq = 2
    partner_hiv_test = (('Yes', u'Yes'), ('No', u'No'), ('not sure', u'I am not sure'), ("Don't want to answer", u"Don't want to answer"))[0][0]
