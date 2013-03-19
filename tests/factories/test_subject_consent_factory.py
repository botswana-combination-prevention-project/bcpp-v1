import factory
from bhp_consent.models import TestSubjectConsent
from base_consent_factory import BaseConsentFactory
from bhp_registration.tests.factories import RegisteredSubjectFactory
from bhp_common.choices import IDENTITY_TYPE


class TestSubjectConsentFactory(BaseConsentFactory):
    FACTORY_FOR = TestSubjectConsent

    registered_subject = factory.SubFactory(RegisteredSubjectFactory)
    user_provided_subject_identifier = None
    identity = factory.Sequence(lambda n: '{0}2{1}'.format(n.rjust(4, '0'), n.rjust(4, '0')))
    identity_type = factory.Iterator(IDENTITY_TYPE, getter=lambda c: c[0])
    confirm_identity = factory.Sequence(lambda n: '{0}2{1}'.format(n.rjust(4, '0'), n.rjust(4, '0')))