import factory
from datetime import date, datetime
from bhp_base_model.tests.factories import BaseUuidModelFactory
from bcpp_subject.models import MonthsThirdPartner


class MonthsThirdPartnerFactory(BaseUuidModelFactory):
    FACTORY_FOR = MonthsThirdPartner

    report_datetime = datetime.today()
    third_last_sex = (('Days', 'Days'), ('Months', 'Months'), ("Don't want to answer", "Don't want to answer"))[0][0]
    third_last_sex_calc = 2
    first_first_sex = (('Days', 'Days'), ('Months', 'Months'), ('Years', 'Years'), ("Don't want to answer", "Don't want to answer"))[0][0]
    first_first_sex_calc = 2
    first_sex_current = (('Yes', 'Yes'), ('No', 'No'), ("Don't want to answer", "Don't want to answer"))[0][0]
    first_relationship = (('Long-term partner', 'Long-term partner (>2 years) or spouse'), ('2 years or spouse', '2 years or spouse'), ('Boyfriend/Girlfriend', 'Boyfriend/Girlfriend'), ('Casual (known) partner', 'Casual (known) partner'), ('One time partner (previously unknown)', 'One time partner (previously unknown)'), ('Commercial sex worker', 'Commercial sex worker'), ('Other, specify:', 'Other, specify:'), ("Don't want to answer", "Don't want to answer"))[0][0]
    concurrent = (('Yes', 'Yes'), ('No', 'No'), ("Don't want to answer", "Don't want to answer"))[0][0]
    goods_exchange = (('Yes', 'Yes'), ('No', 'No'), ("Don't want to answer", "Don't want to answer"))[0][0]
    first_sex_freq = 2
