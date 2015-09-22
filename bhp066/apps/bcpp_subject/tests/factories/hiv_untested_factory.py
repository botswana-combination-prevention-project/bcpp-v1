import factory

from datetime import datetime

from ...models import HivUntested


class HivUntestedFactory(factory.DjangoModelFactory):
    FACTORY_FOR = HivUntested

    report_datetime = datetime.today()
