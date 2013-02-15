from bhp_lab_entry.models import ScheduledLabEntryBucket
from base_scheduled_entry import BaseScheduledEntry


class ScheduledLabEntry(BaseScheduledEntry):

    def set_bucket_model_cls(self):
        self._bucket_model_cls = ScheduledLabEntryBucket
