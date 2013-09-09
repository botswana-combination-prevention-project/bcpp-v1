from bhp_base_model.tests.factories import BaseUuidModelFactory

from bhp_base_test.models import TestScheduledModel


class TestScheduledModelFactory(BaseUuidModelFactory):
    FACTORY_FOR = TestScheduledModel
