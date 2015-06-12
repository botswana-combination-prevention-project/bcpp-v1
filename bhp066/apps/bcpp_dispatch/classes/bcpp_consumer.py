from edc.device.sync.classes import Consumer

from apps.bcpp_tracking.classes import TrackerHelper


class BcppConsumer(Consumer):

    def post_sync(self, using=None, lock_name=None, **kwargs):
        """Overides post_sync to update tracker values."""

        TrackerHelper().update_trackers()
