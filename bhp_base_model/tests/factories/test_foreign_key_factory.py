import factory
from datetime import datetime
from bhp_base_model.models import TestForeignKey
from bhp_base_model.tests.factories import BaseListModelFactory


class TestForeignKeyFactory(BaseListModelFactory):
    FACTORY_FOR = TestForeignKey
