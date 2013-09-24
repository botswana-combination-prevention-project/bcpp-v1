import factory
from bhp_base_test.models import TestRegistration
from bhp_registration.tests.factories import BaseRegistrationFactory


class TestRegistrationFactory(BaseRegistrationFactory):
    FACTORY_FOR = TestRegistration
