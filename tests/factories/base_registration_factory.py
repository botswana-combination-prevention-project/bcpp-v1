import factory
from datetime import datetime
from bhp_base_model.tests.factories import BaseUuidModelFactory
from bhp_registration.tests.factories import RegisteredSubjectFactory


class BaseRegistrationFactory(BaseUuidModelFactory):
    ABSTRACT_FACTORY = True

    registered_subject = factory.SubFactory(RegisteredSubjectFactory)
    registration_datetime = datetime.today()
