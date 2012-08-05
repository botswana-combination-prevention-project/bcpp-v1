import logging
from datetime import datetime
from django.db.models import Max
from dmis_lock import DmisLock
from lab_import_dmis.models import DmisImportHistory


logger = logging.getLogger(__name__)


class NullHandler(logging.Handler):
    def emit(self, record):
        pass
nullhandler = logger.addHandler(NullHandler())


class ImportHistory(object):
    """ Helps track data import from the dmis to the django-lis by managing access to the
    history model DmisImportHistory and the lock class DmisLock.

    * Call start() to get a lock from DmisLock. If a lock is aquired, a instance of model DmisImportHistory is created
      with the current start_datetime.
    * Call finish() when the import is complete to release the lock and update model DmisImportHistory
      instance with the end_datetime.
    """

    def __init__(self, db, lock_name):
        self.dmis_import_history = None
        self.last_import_datetime = None
        self.conditional_clause = None
        self._lock = None
        self.lock_name = lock_name
        self.db = db

    def start(self):
        if not self._lock:
            self._prepare()
        return self._lock is not None

    def finish(self):
        if self._lock:
            self.dmis_import_history.end_datetime = datetime.today()
            self.dmis_import_history.save()
            self._lock.release()
            self._clean_up()

    def _prepare(self):
        """ Tries to get or create an instance of DmisImportHistory locally and lock the
        django-lis for self.lock_name.

        KeyWord Arguments:
            * subject_identifier -- used as the lock name
            * protocol -- used as the lock name
        """
        def get_last_import_datetime(lock_name):
            """ Returns the end datetime of the last successful dmis import for this lock"""
            if DmisImportHistory.objects.using(self.db).filter(lock_name=lock_name, end_datetime__isnull=False):
                agg = DmisImportHistory.objects.using(self.db).filter(lock_name=lock_name).aggregate(Max('end_datetime'))
                retval = agg['end_datetime__max']
            else:
                retval = None
            return retval

        def prepare_clause(last_import_datetime):
            """ Returns a fragment for the sql WHERE clause if last_import_datetime is not None."""
            if last_import_datetime:
                self.conditional_clause = 'l.datelastmodified >= \'{last_import_datetime}\' '.format(last_import_datetime=last_import_datetime.strftime('%Y-%m-%d %H:%M'))

        retval = True
        self._lock = DmisLock(self.db)
        if self._lock.get_lock(self.lock_name):
            if not self.lock_name:
                raise TypeError('Need a lock name. Got None.')
            #if DmisImportHistory.objects.filter(lock_name=self.lock_name, end_datetime__isnull=False):
            #    self.last_import_datetime = get_last_import_datetime(self.lock_name)
            #    self.dmis_import_history = DmisImportHistory.objects.get(lock_name=self.lock_name, end_datetime__isnull=False)
            #elif DmisImportHistory.objects.filter(lock_name=self.lock_name, end_datetime__isnull=True):
            #    # found an open history instance, check if it is locked
            #    self.dmis_import_history = DmisImportHistory.objects.filter(lock_name=self.lock_name, end_datetime__isnull=True).order_by('-start_datetime')[0]
            #    self.last_import_datetime = get_last_import_datetime(self.lock_name)
            #else:
            self.dmis_import_history = DmisImportHistory.objects.using(self.db).create(lock_name=self.lock_name, start_datetime=self._lock.created)
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
        return DmisImportHistory.objects.using(self.db).filter(lock_name=self.lock_name).order_by('-start_datetime')
