import factory
from datetime import date, datetime
from bhp_base_model.tests.factories import BaseUuidModelFactory
from bcpp_subject.models import Stigma


class StigmaFactory(BaseUuidModelFactory):
    FACTORY_FOR = Stigma

    report_datetime = datetime.today()
    anticipate_stigma = (('Strongly disagree', <django.utils.functional.__proxy__ object at 0x103ae2dd0>), ('Disagree', <django.utils.functional.__proxy__ object at 0x103ae2e50>), ('Uncertain', <django.utils.functional.__proxy__ object at 0x103ae2ed0>), ('Agree', <django.utils.functional.__proxy__ object at 0x103ae2f50>), ('Strongly agree', <django.utils.functional.__proxy__ object at 0x103ae2fd0>), ("Don't want to answer", <django.utils.functional.__proxy__ object at 0x103ae4090>))[0][0]
    enacted_shame_stigma = (('Strongly disagree', <django.utils.functional.__proxy__ object at 0x103ae2dd0>), ('Disagree', <django.utils.functional.__proxy__ object at 0x103ae2e50>), ('Uncertain', <django.utils.functional.__proxy__ object at 0x103ae2ed0>), ('Agree', <django.utils.functional.__proxy__ object at 0x103ae2f50>), ('Strongly agree', <django.utils.functional.__proxy__ object at 0x103ae2fd0>), ("Don't want to answer", <django.utils.functional.__proxy__ object at 0x103ae4090>))[0][0]
    saliva_stigma = (('Strongly disagree', <django.utils.functional.__proxy__ object at 0x103ae2dd0>), ('Disagree', <django.utils.functional.__proxy__ object at 0x103ae2e50>), ('Uncertain', <django.utils.functional.__proxy__ object at 0x103ae2ed0>), ('Agree', <django.utils.functional.__proxy__ object at 0x103ae2f50>), ('Strongly agree', <django.utils.functional.__proxy__ object at 0x103ae2fd0>), ("Don't want to answer", <django.utils.functional.__proxy__ object at 0x103ae4090>))[0][0]
    teacher_stigma = (('Strongly disagree', <django.utils.functional.__proxy__ object at 0x103ae2dd0>), ('Disagree', <django.utils.functional.__proxy__ object at 0x103ae2e50>), ('Uncertain', <django.utils.functional.__proxy__ object at 0x103ae2ed0>), ('Agree', <django.utils.functional.__proxy__ object at 0x103ae2f50>), ('Strongly agree', <django.utils.functional.__proxy__ object at 0x103ae2fd0>), ("Don't want to answer", <django.utils.functional.__proxy__ object at 0x103ae4090>))[0][0]
    children_stigma = (('Strongly disagree', <django.utils.functional.__proxy__ object at 0x103ae2dd0>), ('Disagree', <django.utils.functional.__proxy__ object at 0x103ae2e50>), ('Uncertain', <django.utils.functional.__proxy__ object at 0x103ae2ed0>), ('Agree', <django.utils.functional.__proxy__ object at 0x103ae2f50>), ('Strongly agree', <django.utils.functional.__proxy__ object at 0x103ae2fd0>), ("Don't want to answer", <django.utils.functional.__proxy__ object at 0x103ae4090>))[0][0]
