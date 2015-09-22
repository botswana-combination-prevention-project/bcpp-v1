import factory

from datetime import date, datetime

from ...models import Pregnancy


class PregnancyFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Pregnancy

    report_datetime = datetime.today()
    lnmp = date.today()
