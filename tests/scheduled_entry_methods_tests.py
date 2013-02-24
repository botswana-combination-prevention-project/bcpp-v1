from django.test import TestCase
from bhp_entry.models import ScheduledEntryBucket
from bhp_entry.classes import ScheduledEntry


class ScheduledEntryMethodsTests(TestCase):

    def test_set_bucket_model_cls(self):
        scheduled_entry = ScheduledEntry()
        self.assertEquals(scheduled_entry.get_bucket_model_cls(), ScheduledEntryBucket)

#    def test_get_bucket_model_instance(self):
#        scheduled_entry = ScheduledEntry()
#        scheduled_entry.get_bucket_model_instance()