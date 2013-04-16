import factory
from bhp_dispatch.models import TestItemBypassForEdit
from bhp_base_model.tests.factories import BaseUuidModelFactory
from test_container_factory import TestContainerFactory


class TestItemBypassForEditFactory(BaseUuidModelFactory):
    FACTORY_FOR = TestItemBypassForEdit

    test_item_identifier = factory.Sequence(lambda n: 'ITEM_BYPASS_ID{0}'.format(n))
    test_container = factory.SubFactory(TestContainerFactory)
    f1 = factory.Sequence(lambda n: 'F1_{0}'.format(n))
    f2 = factory.Sequence(lambda n: 'F2_{0}'.format(n))
    f3 = factory.Sequence(lambda n: 'F3_{0}'.format(n))
    f4 = factory.Sequence(lambda n: 'F4_{0}'.format(n))
