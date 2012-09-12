import logging
from bhp_lock.classes import BaseLock
from bhp_sync.models import SyncLockModel, SyncImportHistoryModel

logger = logging.getLogger(__name__)


class NullHandler(logging.Handler):
    def emit(self, record):
        pass
nullhandler = logger.addHandler(NullHandler())


class SyncLock(BaseLock):

    def __init__(self, db):
        self.db = db
        super(SyncLock, self).__init__(db, SyncLockModel, SyncImportHistoryModel)
