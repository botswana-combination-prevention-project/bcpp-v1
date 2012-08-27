from bhp_lab_entry.models import ScheduledLabEntryBucket
from base_entry import BaseEntry


class ScheduledLabEntry(BaseEntry):

    def set_bucket_model_cls(self):
        self._bucket_model_cls = ScheduledLabEntryBucket
