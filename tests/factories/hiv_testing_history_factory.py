import factory
from datetime import date, datetime
from bhp_base_model.tests.factories import BaseUuidModelFactory
from bcpp_subject.models import HivTestingHistory


class HivTestingHistoryFactory(BaseUuidModelFactory):
    FACTORY_FOR = HivTestingHistory

    report_datetime = datetime.today()
    has_tested = (('Yes', u'Yes'), ('No', u'No'), ("Don't want to answer", u"Don't want to answer"))[0][0]
    other_record = (('Yes', <django.utils.functional.__proxy__ object at 0x101d48e50>), ('No', <django.utils.functional.__proxy__ object at 0x101d48ed0>))[0][0]
