import factory
from datetime import date, datetime
from bhp_base_model.tests.factories import BaseUuidModelFactory
from bcpp_subject.models import HivResult


class HivResultFactory(BaseUuidModelFactory):
    FACTORY_FOR = HivResult

    report_datetime = datetime.today()
    hiv_result = (('POS', <django.utils.functional.__proxy__ object at 0x103aea110>), ('NEG', <django.utils.functional.__proxy__ object at 0x103aea190>), ('IND', <django.utils.functional.__proxy__ object at 0x103aea210>), ('Declined', <django.utils.functional.__proxy__ object at 0x103aea290>), ('Not performed', <django.utils.functional.__proxy__ object at 0x103aea310>))[0][0]
