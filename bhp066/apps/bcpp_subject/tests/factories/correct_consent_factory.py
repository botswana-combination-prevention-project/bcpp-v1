import factory

from datetime import datetime

from bhp066.apps.bcpp_subject.tests.factories import SubjectConsentFactory

from ...models import CorrectConsent


class CorrectConsentFactory(factory.DjangoModelFactory):
    FACTORY_FOR = CorrectConsent

    subject_consent = factory.SubFactory(SubjectConsentFactory)
    report_datetime = datetime.today()
