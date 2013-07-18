import factory
from datetime import date, datetime
from bhp_base_model.tests.factories import BaseUuidModelFactory
from bcpp_subject.models import HivResult


class HivResultFactory(BaseUuidModelFactory):
    FACTORY_FOR = HivResult

    report_datetime = datetime.today()
    hiv_result = (('POS', 'HIV Positive (Reactive)'), ('NEG', 'HIV Negative (Non-reactive)'), ('IND', 'Indeterminate'), ('Declined', 'Participant declined testing'), ('Not performed', 'Test could not be performed (e.g. supply outage, technical problem)'))[0][0]
