import factory
from datetime import date, datetime

from ...models import LastHivRecord

from htc_subject_visit_factory import HtcSubjectVisitFactory


class LastHivRecordFactory(factory.DjangoModelFactory):
    FACTORY_FOR = LastHivRecord

    htc_subject_visit = factory.SubFactory(HtcSubjectVisitFactory)
    report_datetime = datetime.today()
    recorded_test = date.today()
    recorded_result = 'POS'
    attended_hiv_care = (('Yes', u'Yes'), ('No', u'No'), ('DECLINED', u'Declined to answer'))[0][0]
    hiv_care_card = (('Yes', u'Yes'), ('No', u'No'), ('DECLINED', u'Declined to answer'))[0][0]
