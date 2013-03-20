import factory
from bhp_dispatch.models import TestItem
from bhp_base_model.tests.factories import BaseUuidModelFactory
from test_container_factory import TestContainerFactory


class TestItemFactory(BaseUuidModelFactory):
    FACTORY_FOR = TestItem

    test_item_identifier = factory.Sequence(lambda n: 'ITEM_ID{0}'.format(n))
    test_container = factory.SubFactory(TestContainerFactory)
