import factory
from datetime import date, datetime

from edc.base.model.tests.factories import BaseUuidModelFactory

from ...models import HtcHivTestingHistory

from .htc_subject_visit_factory import HtcSubjectVisitFactory


class HtcHivTestingHistoryFactory(BaseUuidModelFactory):
    FACTORY_FOR = HtcHivTestingHistory

    htc_subject_visit = factory.SubFactory(HtcSubjectVisitFactory)
    report_datetime = datetime.today()
    previous_testing = (('Yes', u'Yes'), ('No', u'No'))[0][0]
