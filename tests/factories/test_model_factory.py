import factory
from datetime import datetime
from bhp_base_model.models import TestModel
from bhp_base_model.tests.factories import BaseUuidModelFactory
from bhp_base_model.tests.factories import TestForeignKeyFactory


class TestModelFactory(BaseUuidModelFactory):
    FACTORY_FOR = TestModel

    name = factory.Sequence(lambda n: 'NAME{0}'.format(n))
    test_foreign_key = factory.SubFactory(TestForeignKeyFactory)
