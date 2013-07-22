import factory
from datetime import date, datetime
from bhp_base_model.tests.factories import BaseUuidModelFactory
from bcpp_subject.models import MonthsSecondPartner


class MonthsSecondPartnerFactory(BaseUuidModelFactory):
    FACTORY_FOR = MonthsSecondPartner

    report_datetime = datetime.today()
    third_last_sex = (('Days', <django.utils.functional.__proxy__ object at 0x103ae4110>), ('Months', <django.utils.functional.__proxy__ object at 0x103ae4190>), ("Don't want to answer", <django.utils.functional.__proxy__ object at 0x103ae4210>))[0][0]
    third_last_sex_calc = 2
    first_first_sex = (('Days', <django.utils.functional.__proxy__ object at 0x103aeda10>), ('Months', <django.utils.functional.__proxy__ object at 0x103aeda90>), ('Years', <django.utils.functional.__proxy__ object at 0x103aedb10>), ("Don't want to answer", <django.utils.functional.__proxy__ object at 0x103aedb90>))[0][0]
    first_first_sex_calc = 2
    first_sex_current = (('Yes', <django.utils.functional.__proxy__ object at 0x103ae2a10>), ('No', <django.utils.functional.__proxy__ object at 0x103ae2ad0>), ("Don't want to answer", <django.utils.functional.__proxy__ object at 0x103ae2b50>))[0][0]
    first_relationship = (('Long-term partner', <django.utils.functional.__proxy__ object at 0x103aedc90>), ('2 years or spouse', <django.utils.functional.__proxy__ object at 0x103aedd10>), ('Boyfriend/Girlfriend', <django.utils.functional.__proxy__ object at 0x103aedd90>), ('Casual (known) partner', <django.utils.functional.__proxy__ object at 0x103aede10>), ('One time partner (previously unknown)', <django.utils.functional.__proxy__ object at 0x103aede90>), ('Commercial sex worker', <django.utils.functional.__proxy__ object at 0x103aedf10>), ('Other, specify:', <django.utils.functional.__proxy__ object at 0x103aedf90>), ("Don't want to answer", <django.utils.functional.__proxy__ object at 0x103aef050>))[0][0]
    concurrent = (('Yes', <django.utils.functional.__proxy__ object at 0x103ae2a10>), ('No', <django.utils.functional.__proxy__ object at 0x103ae2ad0>), ("Don't want to answer", <django.utils.functional.__proxy__ object at 0x103ae2b50>))[0][0]
    goods_exchange = (('Yes', <django.utils.functional.__proxy__ object at 0x103ae2a10>), ('No', <django.utils.functional.__proxy__ object at 0x103ae2ad0>), ("Don't want to answer", <django.utils.functional.__proxy__ object at 0x103ae2b50>))[0][0]
    first_sex_freq = 2
    partner_hiv_test = (('Yes', <django.utils.functional.__proxy__ object at 0x103ae2bd0>), ('No', <django.utils.functional.__proxy__ object at 0x103ae2c50>), ('not sure', <django.utils.functional.__proxy__ object at 0x103ae2cd0>), ("Don't want to answer", <django.utils.functional.__proxy__ object at 0x103ae2d50>))[0][0]
