import factory
from bhp_common.choices import IDENTITY_TYPE
from bhp_base_test.models import TestConsent
from test_consent_factory import BaseConsentFactory


class TestConsentNoRsFactory(BaseConsentFactory):
    FACTORY_FOR = TestConsent

    user_provided_subject_identifier = None
    identity = factory.Sequence(lambda n: '{0}2{1}'.format(str(n).rjust(4, '0'), str(n).rjust(4, '0')))
    identity_type = factory.Iterator(IDENTITY_TYPE, getter=lambda c: c[0])
    confirm_identity = factory.Sequence(lambda n: '{0}2{1}'.format(str(n).rjust(4, '0'), str(n).rjust(4, '0')))
    first_name = factory.Sequence(lambda n: 'JASON{0}'.format(n))
    initials = factory.Sequence(lambda n: 'J{0}W'.format(n))
