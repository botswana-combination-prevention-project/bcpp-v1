import factory
from datetime import date, datetime
from bhp_base_model.tests.factories import BaseUuidModelFactory
from bcpp_subject.models import HivTestingHistory


class HivTestingHistoryFactory(BaseUuidModelFactory):
    FACTORY_FOR = HivTestingHistory

    report_datetime = datetime.today()
    has_tested = (('Yes', 'Yes'), ('No', 'No'), ("Don't want to answer", "Don't want to answer"))[0][0]
    other_record = (('Yes', 'Yes'), ('No', 'No'))[0][0]
