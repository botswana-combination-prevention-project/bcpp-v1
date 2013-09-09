from bhp_lock.models import BaseLockModel


class SyncLockModel(BaseLockModel):

    """ Track which producer's transactions are being received"""

    class Meta:
        app_label = 'bhp_sync'
