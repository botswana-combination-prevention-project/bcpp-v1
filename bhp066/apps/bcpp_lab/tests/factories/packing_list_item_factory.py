from datetime import datetime
import factory
from edc.base.model.tests.factories import BaseUuidModelFactory
from ...models import PackingListItem, PackingList


class PackingListItemFactory(BaseUuidModelFactory):
    FACTORY_FOR = PackingListItem

    packing_list = factory.SubFactory(PackingList)
    item_reference = factory.Sequence(lambda n: 'item_reference{0}'.format(n))