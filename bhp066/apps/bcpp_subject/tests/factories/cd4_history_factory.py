from datetime import datetime
from edc.base.model.tests.factories import BaseUuidModelFactory
from ...models import Cd4History


class Cd4HistoryFactory(BaseUuidModelFactory):
    FACTORY_FOR = Cd4History

    report_datetime = datetime.today()
