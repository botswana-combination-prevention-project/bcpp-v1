import factory
from datetime import date, datetime
from edc.base.model.tests.factories import BaseUuidModelFactory
from ..factories import CallLogFactory
from ...models import CallLogEntry


class CallLogEntryFactory(BaseUuidModelFactory):
    FACTORY_FOR = CallLogEntry

    call_log = factory.SubFactory(CallLogFactory)
    call_datetime = datetime.now()
    contact_type = 'indirect'
    survival_status = 'Alive'
    call_again = 'Yes'