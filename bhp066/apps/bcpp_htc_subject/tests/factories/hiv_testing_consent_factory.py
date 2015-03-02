import factory
from datetime import date, datetime

from edc.base.model.tests.factories import BaseUuidModelFactory

from ...models import HivTestingConsent

from .htc_subject_visit_factory import HtcSubjectVisitFactory


class HivTestingConsentFactory(BaseUuidModelFactory):
    FACTORY_FOR = HivTestingConsent

    htc_subject_visit = factory.SubFactory(HtcSubjectVisitFactory)
    report_datetime = datetime.today()
    testing_today = 'Yes'
