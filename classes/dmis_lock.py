import logging
from django.db.models import Q
from lab_import_dmis.models import DmisLock as DmisLockModel

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

    def get_lock(self, lock_name):
        if not self.lock:
            try:
                self.lock = DmisLockModel.objects.using(self.db).create(lock_name=lock_name)
            except:
                self.lock = None
        return self.lock

    def release(self, lock_name=None):
        """ Release (deletes) a lock.

        May be called to release to release a lock by name without first calling get_lock
        if all you need from the class is to release a lock.
        """
        if lock_name and self.lock is None:
            if DmisLockModel.objects.using(self.db).filter(lock_name=lock_name):
                self.lock = DmisLockModel.objects.using(self.db).get(lock_name=lock_name)
        if self.lock:
            self.lock.delete()
            self.lock = None
            self.is_locked = False
        return self.lock is None

    def check(self):
        return self.is_locked

    def list(self, lock_name=None):
        """ Return a queryset of all locks or just those for given lock name."""
        if lock_name:
            dmis_lock_model = DmisLockModel.objects.using(self.db).filter(lock_name=lock_name)
        else:
            dmis_lock_model = DmisLockModel.objects.using(self.db).filter()
        return dmis_lock_model 