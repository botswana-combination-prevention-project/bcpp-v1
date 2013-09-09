import factory
from bhp_appointment.tests.factories import AppointmentFactory
from bhp_entry.models import ScheduledEntryBucket
from base_entry_bucket_factory import BaseEntryBucketFactory
from entry_factory import EntryFactory


class ScheduledEntryBucketFactory(BaseEntryBucketFactory):
    FACTORY_FOR = ScheduledEntryBucket

    appointment = factory.SubFactory(AppointmentFactory)
    entry = factory.SubFactory(EntryFactory)
