import factory
from datetime import date, datetime
from bhp_base_model.tests.factories import BaseUuidModelFactory
from bcpp_subject.models import SubstanceUse


class SubstanceUseFactory(BaseUuidModelFactory):
    FACTORY_FOR = SubstanceUse

    report_datetime = datetime.today()
    alcohol = (('Never', <django.utils.functional.__proxy__ object at 0x103afafd0>), ('Less then once a week', <django.utils.functional.__proxy__ object at 0x103afb090>), ('Once a week', <django.utils.functional.__proxy__ object at 0x103afb110>), ('2 to 3 times a week', <django.utils.functional.__proxy__ object at 0x103afb190>), ('more than 3 times a week', <django.utils.functional.__proxy__ object at 0x103afb210>), ("Don't want to answer", <django.utils.functional.__proxy__ object at 0x103afb290>))[0][0]
    smoke = (('Yes', <django.utils.functional.__proxy__ object at 0x103ae2a10>), ('No', <django.utils.functional.__proxy__ object at 0x103ae2ad0>), ("Don't want to answer", <django.utils.functional.__proxy__ object at 0x103ae2b50>))[0][0]
