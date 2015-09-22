import factory
from datetime import datetime

from ...models import HivTestingConsent

from .htc_subject_visit_factory import HtcSubjectVisitFactory


class HivTestingConsentFactory(factory.DjangoModelFactory):
    FACTORY_FOR = HivTestingConsent

    htc_subject_visit = factory.SubFactory(HtcSubjectVisitFactory)
    report_datetime = datetime.today()
    testing_today = 'Yes'
