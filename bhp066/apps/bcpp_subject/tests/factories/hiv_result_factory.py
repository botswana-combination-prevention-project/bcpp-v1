import factory
from datetime import date, datetime
from edc.base.model.tests.factories import BaseUuidModelFactory
from apps.bcpp_subject.models import HivResult


class HivResultFactory(BaseUuidModelFactory):
    FACTORY_FOR = HivResult

    report_datetime = datetime.today()
    hiv_result = (('POS', u'HIV Positive (Reactive)'), ('NEG', u'HIV Negative (Non-reactive)'), ('IND', u'Indeterminate'), ('Declined', u'Participant declined testing'), ('Not performed', u'Test could not be performed (e.g. supply outage, technical problem)'))[0][0]
