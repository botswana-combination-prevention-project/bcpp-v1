import factory
from datetime import date, datetime
from bhp_base_model.tests.factories import BaseUuidModelFactory
from bcpp_subject.models import ReproductiveHealth


class ReproductiveHealthFactory(BaseUuidModelFactory):
    FACTORY_FOR = ReproductiveHealth

    report_datetime = datetime.today()
    number_children = 2
    menopause = (('Yes', <django.utils.functional.__proxy__ object at 0x101d48e50>), ('No', <django.utils.functional.__proxy__ object at 0x101d48ed0>))[0][0]
    family_planning_other = factory.Sequence(lambda n: 'family_planning_other{0}'.format(n))
