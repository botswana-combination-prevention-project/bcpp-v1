import logging
from lab_import.classes import BaseLock
from lab_import_dmis.models import DmisLock as DmisLockModel, DmisImportHistory

logger = logging.getLogger(__name__)


class NullHandler(logging.Handler):
    def emit(self, record):
        pass
nullhandler = logger.addHandler(NullHandler())


class DmisLock(BaseLock):

    def __init__(self, db):
        self.db = db
        super(DmisLock, self).__init__(db, DmisLockModel, DmisImportHistory)
