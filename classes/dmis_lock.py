import logging
from lab_import_dmis.models import DmisLock as DmisLockModel, DmisImportHistory

logger = logging.getLogger(__name__)


class NullHandler(logging.Handler):
    def emit(self, record):
        pass
nullhandler = logger.addHandler(NullHandler())


class DmisLock(object):
    """ Locks out others from initiating a dmis import for the given protocol or subject. """

    def __init__(self, db):
        self.db = db
        self.lock = None
        self.is_locked = False

    @property
    def created(self):
        if self.lock:
            return self.lock.created
        return None

    def get_lock(self, lock_name):
        if not self.lock:
            try:
                self.lock = DmisLockModel.objects.using(self.db).create(lock_name=lock_name)
            except:
                self.lock = None
                logger.warning('  Warning: Unable to set a lock to import from dmis for {0}. '
                               'One already exists.'.format(lock_name))
        return self.lock

    def release(self, lock_name=None):
        """ Release (deletes) a lock.

        May be called to release a lock by name without first calling get_lock
        if all you need from the class is to release a lock.
        """
        if lock_name and self.lock is None:
            if DmisLockModel.objects.using(self.db).filter(lock_name=lock_name):
                self.lock = DmisLockModel.objects.using(self.db).get(lock_name=lock_name)
                DmisImportHistory.objects.using(self.db).filter(lock_name=lock_name, end_datetime__isnull=True).delete()
                logger.info('  Removed incomplete history record(s) for lock {0}.'.format(lock_name))

        if self.lock:
            self.lock.delete()
            logger.info('  Lock {0} has been released.'.format(lock_name))
            self.lock = None
            self.is_locked = False
        else:
            logger.info('  Lock {0} does not exist.'.format(lock_name))
        return self.lock is None

    def check(self):
        return self.is_locked

    def list(self, lock_name=None):
        """ Return an ordered queryset of all locks or just those for given lock name."""
        if lock_name:
            dmis_lock_model = DmisLockModel.objects.using(self.db).filter(lock_name=lock_name).order_by('-created')
        else:
            dmis_lock_model = DmisLockModel.objects.using(self.db).filter().order_by('-created')
        return dmis_lock_model 