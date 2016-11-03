from edc.device.sync.classes import Consumer


class BcppConsumer(Consumer):

    def post_sync(self, using=None, lock_name=None, **kwargs):
        """Overides post_sync to update tracker values."""
