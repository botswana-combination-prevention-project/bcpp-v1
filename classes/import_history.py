import logging
from bhp_lock.classes import BaseImportHistory
from bhp_sync.models import SyncImportHistoryModel
from sync_lock import SyncLock


logger = logging.getLogger(__name__)


class NullHandler(logging.Handler):
    def emit(self, record):
        pass
nullhandler = logger.addHandler(NullHandler())


class ImportHistory(BaseImportHistory):

    def __init__(self, db, lock_name):
        super(ImportHistory, self).__init__(db, lock_name, SyncLock, SyncImportHistoryModel)
