import factory

from datetime import datetime

from ...models import Pima


class PimaFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Pima

    report_datetime = datetime.today()
    pima_today = 'Yes'
    pima_id = factory.Sequence(lambda n: 'pima_id{0}'.format(n))
    cd4_value = 2.5
