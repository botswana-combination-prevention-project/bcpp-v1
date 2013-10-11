import factory
from datetime import date, datetime
from edc.base.model.tests.factories import BaseUuidModelFactory
from ...models import Circumcised


class CircumcisedFactory(BaseUuidModelFactory):
    FACTORY_FOR = Circumcised

    report_datetime = datetime.today()
