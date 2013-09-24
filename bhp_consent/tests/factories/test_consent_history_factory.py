import factory
from datetime import datetime
from bhp_base_model.tests.factories import BaseUuidModelFactory
from bhp_base_test.models import TestConsentHistory


class TestConsentHistoryFactory(BaseUuidModelFactory):
    FACTORY_FOR = TestConsentHistory
