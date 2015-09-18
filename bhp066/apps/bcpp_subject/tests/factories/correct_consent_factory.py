import factory
from datetime import datetime, date
from edc.base.model.tests.factories import BaseUuidModelFactory
from bhp066.apps.bcpp_subject.tests.factories import SubjectConsentFactory
from ...models import CorrectConsent


class CorrectConsentFactory(BaseUuidModelFactory):
    FACTORY_FOR = CorrectConsent

    subject_consent = factory.SubFactory(SubjectConsentFactory)
    report_datetime = datetime.today()