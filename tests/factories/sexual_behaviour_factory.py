import factory
from datetime import date, datetime
from bhp_base_model.tests.factories import BaseUuidModelFactory
from bcpp_subject.models import SexualBehaviour


class SexualBehaviourFactory(BaseUuidModelFactory):
    FACTORY_FOR = SexualBehaviour

    report_datetime = datetime.today()
    ever_sex = (('Yes', <django.utils.functional.__proxy__ object at 0x103ae2a10>), ('No', <django.utils.functional.__proxy__ object at 0x103ae2ad0>), ("Don't want to answer", <django.utils.functional.__proxy__ object at 0x103ae2b50>))[0][0]
