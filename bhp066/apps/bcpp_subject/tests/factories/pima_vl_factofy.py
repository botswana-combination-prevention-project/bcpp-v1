import factory
from datetime import date, datetime
from .base_scheduled_model_factory import BaseScheduledModelFactory
from ...models import PimaVl


class PimaVlFactory(BaseScheduledModelFactory):
    FACTORY_FOR = PimaVl
    report_datetime = datetime.today()
    poc_vl_today = 'Yes'
    poc_vl_type = 'mobile setting'
    cd4_datetime = datetime.today()
    time_of_test = datetime.today()
    time_of_result = datetime.today()
    easy_of_use = 'easy'
    pima_id = factory.Sequence(lambda n: 'pima_id{0}'.format(n))
    cd4_value = 1000
