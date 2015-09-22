import factory

from datetime import datetime

from subject_visit_factory import SubjectVisitFactory

from ...models import HivTestingHistory


class HivTestingHistoryFactory(factory.DjangoModelFactory):
    FACTORY_FOR = HivTestingHistory

    subject_visit = factory.SubFactory(SubjectVisitFactory)
    report_datetime = datetime.today()
    has_tested = (('Yes', u'Yes'), ('No', u'No'), ('not_answering', u"Don't want to answer"))[0][0]
    has_record = 'Yes'
    verbal_hiv_result = 'NEG'
    other_record = 'No'
