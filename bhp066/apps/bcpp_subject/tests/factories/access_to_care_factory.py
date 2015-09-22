import factory

from datetime import datetime

from ...models import AccessToCare


class AccessToCareFactory(factory.DjangoModelFactory):
    FACTORY_FOR = AccessToCare

    report_datetime = datetime.today()
