import factory

from datetime import datetime

from ..factories import CallLogFactory
from ...models import CallLogEntry


class CallLogEntryFactory(factory.DjangoModelFactory):
    FACTORY_FOR = CallLogEntry

    call_log = factory.SubFactory(CallLogFactory)
    call_datetime = datetime.now()
    contact_type = 'indirect'
    survival_status = 'Alive'
    call_again = 'Yes'
