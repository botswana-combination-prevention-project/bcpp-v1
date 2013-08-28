from bhp_base_model.tests.factories import BaseUuidModelFactory
from bhp_sync.models import TestItem


class TestItemFactory(BaseUuidModelFactory):
    FACTORY_FOR = TestItem
