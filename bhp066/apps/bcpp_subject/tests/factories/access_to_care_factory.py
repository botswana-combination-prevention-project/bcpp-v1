from datetime import datetime
from edc.base.model.tests.factories import BaseUuidModelFactory
from ...models import AccessToCare


class AccessToCareFactory(BaseUuidModelFactory):
    FACTORY_FOR = AccessToCare

    report_datetime = datetime.today()
