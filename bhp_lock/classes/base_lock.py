import logging
from django.db import DatabaseError, IntegrityError

logger = logging.getLogger(__name__)


class NullHandler(logging.Handler):
    def emit(self, record):
        pass
nullhandler = logger.addHandler(NullHandler())


class BaseLock(object):
    """ Locks out others from initiating an data import for the given protocol or subject. """

    def __init__(self, db, lock_model, import_history_model):
        self.db = db
        self.lock = None
        self.lock_name = None
        self.lock_model = lock_model
        self.import_history_model = import_history_model

    @property
    def created(self):
        if self.lock:
            return self.lock.created
        return None

    @property
    def locked(self):
        retval = False
        if self.lock:
            if self.lock_model.objects.using(self.db).filter(lock_name=self.lock_name):
                retval = True
        return retval

    def get_lock(self, lock_name):
        if not self.lock:
            try:
                self.lock = self.lock_model.objects.using(self.db).create(lock_name=lock_name)
                self.lock_name = lock_name
            except IntegrityError:
                self.lock = None
                logger.warning('  Warning: Unable to set a lock to import for {0}. '
                               'One already exists.'.format(lock_name))
            except DatabaseError as e:
                raise e
            except:
                raise
        return self.lock

    def release(self, lock_name=None):
        """ Release (deletes) a lock.

        May be called to release a lock by name without first calling get_lock
        if all you need from the class is to release a lock.
        """
        if lock_name and self.lock is None:
            if self.lock_model.objects.using(self.db).filter(lock_name=lock_name):
                self.lock = self.lock_model.objects.using(self.db).get(lock_name=lock_name)
                self.import_history_model.objects.using(self.db).filter(lock_name=lock_name, end_datetime__isnull=True).delete()
                logger.info('  Removed incomplete history record(s) for lock {0}.'.format(lock_name))

        if self.lock:
            self.lock.delete()
            logger.info('  Lock {0} has been released.'.format(lock_name or self.lock_name))
            self.lock = None
        else:
            logger.info('  Lock {0} does not exist.'.format(lock_name))
        return self.lock is None

    def list(self, lock_name=None):
        """ Return an ordered queryset of all locks or just those for given lock name."""
        if lock_name:
            lock_model_queryset = self.lock_model.objects.using(self.db).filter(lock_name=lock_name).order_by('-created')
        else:
            lock_model_queryset = self.lock_model.objects.using(self.db).filter().order_by('-created')
        return lock_model_queryset
