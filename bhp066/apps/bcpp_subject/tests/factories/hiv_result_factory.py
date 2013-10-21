import factory
from datetime import date, datetime

from ...models import HivResult

from .base_scheduled_model_factory import BaseScheduledModelFactory


class HivResultFactory(BaseScheduledModelFactory):
    FACTORY_FOR = HivResult

    report_datetime = datetime.today()
    hiv_result = (('POS', u'HIV Positive (Reactive)'), ('NEG', u'HIV Negative (Non-reactive)'), ('IND', u'Indeterminate'), ('Declined', u'Participant declined testing'), ('Not performed', u'Test could not be performed (e.g. supply outage, technical problem)'))[0][0]
