import factory
from datetime import date, datetime
from edc.base.model.tests.factories import BaseUuidModelFactory
from ...models import Pregnancy


class PregnancyFactory(BaseUuidModelFactory):
    FACTORY_FOR = Pregnancy

    report_datetime = datetime.today()
    lnmp = date.today()
