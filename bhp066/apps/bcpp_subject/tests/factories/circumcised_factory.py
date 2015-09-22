import factory

from datetime import datetime

from ...models import Circumcised


class CircumcisedFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Circumcised

    report_datetime = datetime.today()
