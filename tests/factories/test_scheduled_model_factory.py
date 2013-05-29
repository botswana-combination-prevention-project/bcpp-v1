from bhp_base_model.tests.factories import BaseUuidModelFactory

from bhp_visit_tracking.models import TestScheduledModel


class TestScheduledModelFactory(BaseUuidModelFactory):
    FACTORY_FOR = TestScheduledModel
