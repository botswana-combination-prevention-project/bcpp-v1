import logging
from bhp_lab_entry.classes import UnscheduledLabEntry
from bhp_lab_entry.models import UnscheduledLabEntryBucket
from scheduled_data_rule import ScheduledDataRule

logger = logging.getLogger(__name__)


class NullHandler(logging.Handler):
    def emit(self, record):
        pass
nullhandler = logger.addHandler(NullHandler())


class UnscheduledLabRule(ScheduledDataRule):
    """For rules that add an unscheduled lab."""
    def set_entry_cls(self):
        self._entry_cls = UnscheduledLabEntry

    def set_bucket_cls(self):
        self._bucket_cls = UnscheduledLabEntryBucket
