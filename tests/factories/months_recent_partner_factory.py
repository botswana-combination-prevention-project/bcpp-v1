import factory
from datetime import date, datetime
from bcpp_subject.tests.factories import SubjectVisitFactory
from base_scheduled_model_factory import BaseScheduledModelFactory
from bcpp_subject.models import MonthsRecentPartner


class MonthsRecentPartnerFactory(BaseScheduledModelFactory):
    FACTORY_FOR = MonthsRecentPartner

    subject_visit = factory.SubFactory(SubjectVisitFactory)

    report_datetime = datetime.today()
    third_last_sex = (('Days', 'Days'), ('Months', 'Months'), ("Don't want to answer", "Don't want to answer"))[0][0]
    third_last_sex_calc = 1
    first_first_sex = (('Days', 'Days'), ('Months', 'Months'), ('Years', 'Years'), ("Don't want to answer", "Don't want to answer"))[0][0]
    first_first_sex_calc = 1
    first_sex_current = (('Yes', 'Yes'), ('No', 'No'), ("Don't want to answer", "Don't want to answer"))[0][0]
    first_relationship = (('Long-term partner', 'Long-term partner (>2 years) or spouse'), ('2 years or spouse', '2 years or spouse'), ('Boyfriend/Girlfriend', 'Boyfriend/Girlfriend'), ('Casual (known) partner', 'Casual (known) partner'), ('One time partner (previously unknown)', 'One time partner (previously unknown)'), ('Commercial sex worker', 'Commercial sex worker'), ('Other, specify:', 'Other, specify:'), ("Don't want to answer", "Don't want to answer"))[0][0]
    concurrent = (('Yes', 'Yes'), ('No', 'No'), ("Don't want to answer", "Don't want to answer"))[0][0]
    goods_exchange = (('Yes', 'Yes'), ('No', 'No'), ("Don't want to answer", "Don't want to answer"))[0][0]
    first_sex_freq = 1
