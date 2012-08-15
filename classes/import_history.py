import logging
from lab_import.classes import BaseImportHistory
from lab_import_dmis.models import DmisImportHistoryModel
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
        self._lock = None
        self.lock_name = lock_name
        self.db = db
        super(ImportHistory, self).__init__(db, lock_name, DmisLock, DmisImportHistoryModel)

    @property
    def clause(self):
        clause = self._prepare_clause
        return clause

    def _prepare_clause(self):
        """ Returns a fragment for the sql WHERE clause if last_import_datetime is not None."""
        conditional_clause = ''
        if self.last_import_datetime:
            conditional_clause = (' (l.datelastmodified >= \'{last_import_datetime}\' or '
                                  'l21.datelastmodified >= \'{last_import_datetime}\') ').format(last_import_datetime=self.last_import_datetime.strftime('%Y-%m-%d %H:%M'))
        return conditional_clause
