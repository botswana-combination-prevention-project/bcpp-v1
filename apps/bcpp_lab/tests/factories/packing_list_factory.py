from datetime import datetime
import factory
from edc.base.model.tests.factories import BaseUuidModelFactory
from ...models import PackingList


class PackingListFactory(BaseUuidModelFactory):
    FACTORY_FOR = PackingList

    list_datetime = datetime.today()
    list_items = factory.Sequence(lambda n: 'list_items{0}'.format(n))