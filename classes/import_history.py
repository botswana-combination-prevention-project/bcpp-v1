import logging
from lab_import.classes import BaseImportHistory
from lab_import_dmis.models import DmisImportHistory
from dmis_lock import DmisLock


logger = logging.getLogger(__name__)


class NullHandler(logging.Handler):
    def emit(self, record):
        pass
nullhandler = logger.addHandler(NullHandler())


class ImportHistory(BaseImportHistory):

    def __init__(self, db, lock_name):
        self.dmis_import_history = None
        self.last_import_datetime = None
        self.conditional_clause = None
        self._lock = None
        self.lock_name = lock_name
        self.db = db
        super(ImportHistory, self).__init__(db, lock_name, DmisLock, DmisImportHistory)
