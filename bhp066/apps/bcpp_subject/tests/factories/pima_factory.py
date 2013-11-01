import factory
from datetime import date, datetime
from edc.base.model.tests.factories import BaseUuidModelFactory
from ...models import Pima


class PimaFactory(BaseUuidModelFactory):
    FACTORY_FOR = Pima

    report_datetime = datetime.today()
    pima_today = 'Yes'
    pima_id = factory.Sequence(lambda n: 'pima_id{0}'.format(n))
    cd4_value = 2.5
