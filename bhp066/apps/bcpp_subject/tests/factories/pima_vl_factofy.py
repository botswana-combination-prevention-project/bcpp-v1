import factory
from datetime import date, datetime
from edc.base.model.tests.factories import BaseUuidModelFactory
from ...models import PimaVl


class PimaVlFactory(BaseUuidModelFactory):
    FACTORY_FOR = PimaVl

    report_datetime = datetime.today()
    pima_today = 'Yes'
    poc_vl_type = 'mobile setting'
    cd4_datetime = datetime.today()
    time_of_test = datetime.today()
    time_of_result = datetime.today()
    easy_of_use = 'easy'
    pima_id = factory.Sequence(lambda n: 'pima_id{0}'.format(n))
    cd4_value = 2.5
