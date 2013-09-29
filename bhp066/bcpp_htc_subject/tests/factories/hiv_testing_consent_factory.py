import factory
from datetime import date, datetime
from bhp_base_model.tests.factories import BaseUuidModelFactory
from bcpp_htc_subject.models import HivTestingConsent
from htc_subject_visit_factory import HtcSubjectVisitFactory


class HivTestingConsentFactory(BaseUuidModelFactory):
    FACTORY_FOR = HivTestingConsent

    htc_subject_visit = factory.SubFactory(HtcSubjectVisitFactory)
    report_datetime = datetime.today()
    testing_today = 'Yes'
