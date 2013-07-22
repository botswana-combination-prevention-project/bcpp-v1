import factory
from datetime import date, datetime
from bhp_base_model.tests.factories import BaseUuidModelFactory
from bcpp_subject.models import HivTested


class HivTestedFactory(BaseUuidModelFactory):
    FACTORY_FOR = HivTested

    report_datetime = datetime.today()
    where_hiv_test = (('Tebelopele VCT center', <django.utils.functional.__proxy__ object at 0x103aeb0d0>), ('Antenatal care at healthcare facility', <django.utils.functional.__proxy__ object at 0x103aeb150>), ('Other (not antenatal care) at healthcare facility', <django.utils.functional.__proxy__ object at 0x103aeb1d0>), ('In my house as part of door-to-door services', <django.utils.functional.__proxy__ object at 0x103aeb250>), ('In a mobile tent or vehicle in my neighborhood', <django.utils.functional.__proxy__ object at 0x103aeb2d0>), ('Other, specify:', <django.utils.functional.__proxy__ object at 0x103aeb350>), ('I am not sure', <django.utils.functional.__proxy__ object at 0x103aeb3d0>), ("Don't want to answer", <django.utils.functional.__proxy__ object at 0x103aeb450>))[0][0]
