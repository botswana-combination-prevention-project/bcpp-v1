import factory
from datetime import date, datetime
from edc.base.model.tests.factories import BaseUuidModelFactory
from ...models import Pima


class PimaFactory(BaseUuidModelFactory):
    FACTORY_FOR = Pima

    report_datetime = datetime.today()
    pima_id = factory.Sequence(lambda n: 'pima_id{0}'.format(n))
    cd4_value = 2.5
    draw_time = datetime.today().strftime('%H:%m')
    is_drawn = (('Yes', '<django.utils.functional.__proxy__ object at 0x1021b8810>'), ('No', '<django.utils.functional.__proxy__ object at 0x1021b8850>'))[0][0]
