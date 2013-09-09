import factory
from bhp_base_model.tests.factories import BaseUuidModelFactory
from bhp_registration.tests.factories import RegisteredSubjectFactory


class BaseEntryBucketFactory(BaseUuidModelFactory):
    ABSTRACT_FACTORY = True

    registered_subject = factory.SubFactory(RegisteredSubjectFactory)
    entry_status = 'NEW'
