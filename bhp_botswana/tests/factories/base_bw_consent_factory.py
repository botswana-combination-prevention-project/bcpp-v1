import factory
from bhp_consent.tests.factories import BaseConsentFactory


class BaseBwConsentFactory(BaseConsentFactory):
    ABSTRACT_FACTORY = True

    identity = factory.Sequence(lambda n: '11111111{0}'.format(n))
    identity_type = 'OMANG'
    confirm_identity = factory.Sequence(lambda n: '11111111{0}'.format(n))
