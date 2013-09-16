import factory
from datetime import datetime
from bhp_base_model.models import TestManyToMany
from bhp_base_model.tests.factories import BaseListModelFactory


class TestManyToManyFactory(BaseListModelFactory):
    FACTORY_FOR = TestManyToMany
