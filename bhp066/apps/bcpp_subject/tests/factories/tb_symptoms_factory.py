import factory

from datetime import datetime

from ...models import TbSymptoms


class TbSymptomsFactory(factory.DjangoModelFactory):
    FACTORY_FOR = TbSymptoms

    report_datetime = datetime.today()
    cough = 'Yes'
    cough_blood = 'Yes'
    night_sweat = 'Yes'
    weight_loss = 'No'
    fever = 'No'
