import logging
from lab_import.classes import BaseLock
from lab_clinic_api.models import LockModel, ImportHistoryModel

logger = logging.getLogger(__name__)


class NullHandler(logging.Handler):
    def emit(self, record):
        pass
nullhandler = logger.addHandler(NullHandler())


class LisLock(BaseLock):

    def __init__(self, db):
        self.db = db
        super(LisLock, self).__init__(db, LockModel, ImportHistoryModel)
