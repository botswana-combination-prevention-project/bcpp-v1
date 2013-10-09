import factory
from datetime import date, datetime
from edc.base.model.tests.factories import BaseUuidModelFactory
from ...models import HivUntested


class HivUntestedFactory(BaseUuidModelFactory):
    FACTORY_FOR = HivUntested

    report_datetime = datetime.today()
