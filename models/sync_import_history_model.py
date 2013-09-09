from bhp_lock.models import BaseImportHistoryModel


class SyncImportHistoryModel(BaseImportHistoryModel):

    class Meta:
        app_label = 'bhp_sync'
