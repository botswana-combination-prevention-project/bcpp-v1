import factory
from bhp_dispatch.models import TestContainer
from bhp_base_model.tests.factories import BaseUuidModelFactory


class TestContainerFactory(BaseUuidModelFactory):
    FACTORY_FOR = TestContainer

    test_container_identifier = factory.Sequence(lambda n: 'CONTAINER_ID{0}'.format(n))
    comment = 'test_container'
