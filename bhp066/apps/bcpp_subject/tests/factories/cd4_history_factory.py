import factory

from datetime import datetime

from ...models import Cd4History


class Cd4HistoryFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Cd4History

    report_datetime = datetime.today()
