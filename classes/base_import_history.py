import logging
from datetime import datetime
from django.db.models import Max


logger = logging.getLogger(__name__)


class NullHandler(logging.Handler):
    def emit(self, record):
        pass
nullhandler = logger.addHandler(NullHandler())


class BaseImportHistory(object):
    """ Helps track data import from the dmis to the django-lis by managing access to the
    history model self.import_history_model and the lock class obj_lock.

    * Call start() to get a lock from obj_lock. If a lock is aquired, a instance of model self.import_history_model is created
      with the current start_datetime.
    * Call finish() when the import is complete to release the lock and update model self.import_history_model
      instance with the end_datetime.
    """

    def __init__(self, db, lock_name, obj_lock, import_history_model):
        self.dmis_import_history = None
        self.last_import_datetime = None
        self.conditional_clause = None
        self._lock = None
        self.obj_lock = obj_lock
        self.lock_name = lock_name
        self.import_history_model = import_history_model
        self.db = db

    @property
    def locked(self):
        return self._lock.locked

    @property
    def clause(self):
        return self.conditional_clause

    def start(self):
        if not self._lock:
            self._prepare()
        return self._lock is not None

    def finish(self):
        if self._lock:
            # only update the history if the lock still exists in the db,
            # as someone may have deleted it to stop the process
            # before was able to completed
            if self.locked:
                self.dmis_import_history.end_datetime = datetime.today()
                self.dmis_import_history.save()
            else:
                self.dmis_import_history.delete()
            self._lock.release()
            self._clean_up()

    def _prepare(self):
        """ Tries to get or create an instance of self.import_history_model locally and lock the
        django-lis for self.lock_name.

        KeyWord Arguments:
            * subject_identifier -- used as the lock name
            * protocol -- used as the lock name
        """
        def get_last_import_datetime(lock_name):
            """ Returns the end datetime of the last successful dmis import for this lock"""
            if self.import_history_model.objects.using(self.db).filter(lock_name=lock_name, end_datetime__isnull=False):
                agg = self.import_history_model.objects.using(self.db).filter(lock_name=lock_name).aggregate(Max('end_datetime'))
                retval = agg['end_datetime__max']
            else:
                retval = None
            return retval

        def prepare_clause(last_import_datetime):
            """ Returns a fragment for the sql WHERE clause if last_import_datetime is not None."""
            if last_import_datetime:
                self.conditional_clause = (' (l.datelastmodified >= \'{last_import_datetime}\' or '
                                           'l21.datelastmodified >= \'{last_import_datetime}\') ').format(last_import_datetime=last_import_datetime.strftime('%Y-%m-%d %H:%M'))

        retval = True
        self._lock = self.obj_lock(self.db)
        if self._lock.get_lock(self.lock_name):
            if not self.lock_name:
                raise TypeError('Need a lock name. Got None.')
            #if self.import_history_model.objects.filter(lock_name=self.lock_name, end_datetime__isnull=False):
            #    self.last_import_datetime = get_last_import_datetime(self.lock_name)
            #    self.dmis_import_history = self.import_history_model.objects.get(lock_name=self.lock_name, end_datetime__isnull=False)
            #elif self.import_history_model.objects.filter(lock_name=self.lock_name, end_datetime__isnull=True):
            #    # found an open history instance, check if it is locked
            #    self.dmis_import_history = self.import_history_model.objects.filter(lock_name=self.lock_name, end_datetime__isnull=True).order_by('-start_datetime')[0]
            #    self.last_import_datetime = get_last_import_datetime(self.lock_name)
            #else:
            self.dmis_import_history = self.import_history_model.objects.using(self.db).create(lock_name=self.lock_name, start_datetime=self._lock.created)
            self.dmis_import_history.save()
            self.last_import_datetime = get_last_import_datetime(self.lock_name)
            if self.last_import_datetime:
                prepare_clause(self.last_import_datetime)
        else:
            self._clean_up()
            retval = False
        return retval

    def _clean_up(self):
        """ Sets everything to None."""
        self.dmis_import_history = None
        self.last_import_datetime = None,
        self.conditional_clause = None
        self._lock = None

    def history(self):
        return self.import_history_model.objects.using(self.db).filter(lock_name=self.lock_name).order_by('-start_datetime')
