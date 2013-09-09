import factory
from bhp_subject.tests.factories import BaseSubjectFactory
from bhp_registration.models import RegisteredSubject


class RegisteredSubjectFactory(BaseSubjectFactory):
    FACTORY_FOR = RegisteredSubject

    identity = factory.Sequence(lambda n: '11111111{0}'.format(n))
    identity_type = 'OMANG'
    may_store_samples = 'Yes'
    subject_type = 'test_subject_type'
