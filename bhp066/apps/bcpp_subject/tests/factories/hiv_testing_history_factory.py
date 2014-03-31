import factory
from datetime import date, datetime
from edc.base.model.tests.factories import BaseUuidModelFactory
from ...models import HivTestingHistory


class HivTestingHistoryFactory(BaseUuidModelFactory):
    FACTORY_FOR = HivTestingHistory

    report_datetime = datetime.today()
    #has_tested = (('Yes', u'Yes'), ('No', u'No'), ('not_answering', u"Don't want to answer"))[0][0]
