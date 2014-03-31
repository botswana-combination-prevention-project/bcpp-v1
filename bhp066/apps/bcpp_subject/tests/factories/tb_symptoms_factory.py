from datetime import datetime

from edc.base.model.tests.factories import BaseUuidModelFactory

from ...models import TbSymptoms


class TbSymptomsFactory(BaseUuidModelFactory):
    FACTORY_FOR = TbSymptoms

    report_datetime = datetime.today()
    cough = 'Yes'
    cough_blood = 'Yes'
    night_sweat = 'Yes'
    weight_loss = 'No'
    fever = 'No'
