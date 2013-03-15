import factory
from datetime import datetime
from bhp_registration.models import RegisteredSubject


class RegisteredSubjectFactory(factory.DjangoModelFactory):
    FACTORY_FOR = RegisteredSubject

