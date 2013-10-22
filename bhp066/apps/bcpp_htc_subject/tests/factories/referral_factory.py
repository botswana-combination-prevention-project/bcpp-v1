import factory
from datetime import date, datetime

from edc.base.model.tests.factories import BaseUuidModelFactory

from ...models import Referral

from .htc_subject_visit_factory import HtcSubjectVisitFactory


class ReferralFactory(BaseUuidModelFactory):
    FACTORY_FOR = Referral

    htc_subject_visit = factory.SubFactory(HtcSubjectVisitFactory)
    report_datetime = datetime.today()
