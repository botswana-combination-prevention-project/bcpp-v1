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

    def __init__(self, db, lock_name):
        self.dmis_import_history = None
        self.last_import_datetime = None
        self.conditional_clause = None
        self.started = False
        self.lock_name = lock_name
        self.lock = DmisLock(db)

    def start(self, **kwargs):
        if not self.started:
            if self._prepare(**kwargs):
                self.started = True
            else:
                self.started = False

    def finish(self):
        if not self.started:
            raise TypeError('Call start before finish.')
        else:
            self.dmis_import_history.end_datetime = datetime.today()
            self.dmis_import_history.save()
            self.lock.release()
            self._clean_up()

    def _prepare(self, **kwargs):
        """ Tries to get or create an instance of DmisImportHistory locally and lock the django-lis for this lock_name.

        KeyWord Arguments:
            * subject_identifier -- used as the lock name
            * protocol -- used as the lock name
        """
        def get_last_import_datetime(lock_name):
            """ Returns the end datetime of the last successful dmis import for this lock"""
            if DmisImportHistory.objects.filter(lock_name=lock_name, end_datetime__isnull=False):
                agg = DmisImportHistory.objects.filter(lock_name=lock_name).aggregate(Max('end_datetime'))
                retval = agg['end_datetime__max']
            else:
                retval = None
            return retval

        def prepare_clause(last_import_datetime):
            """ Returns a fragment for the sql WHERE clause if last_import_datetime is not None."""
            if last_import_datetime:
                self.conditional_clause = 'l.datelastmodified >= \'{last_import_datetime}\' '.format(last_import_datetime=last_import_datetime.strftime('%Y-%m-%d %H:%M'))

        retval = True
        if not self.lock_name:
            raise TypeError('Need either protocol or subject_identifier. Got None.')
        if DmisImportHistory.objects.filter(lock_name=self.lock_name, end_datetime__isnull=False):
            if self.lock.get_lock(self.lock_name):
                self.last_import_datetime = get_last_import_datetime(self.lock_name)
                self.dmis_import_history = DmisImportHistory.objects.get(lock_name=self.lock_name, end_datetime__isnull=False)
        elif DmisImportHistory.objects.filter(lock_name=self.lock_name, end_datetime__isnull=True):
            # found an open history instance, check if it is locked
            if self.lock.get_lock(self.lock_name):
                self.dmis_import_history = DmisImportHistory.objects.filter(lock_name=self.lock_name, end_datetime__isnull=True).order_by('-start_datetime')[0]
                self.last_import_datetime = get_last_import_datetime(self.lock_name)
            else:
                self.dmis_import_history = None
                logger.info('Unable to lock django-lis to import from django-lis for lock_name {0}.'.format(self.lock_name))
                retval = False
        else:
            self.dmis_import_history = DmisImportHistory.objects.create(lock_name=self.lock_name)
            self.dmis_import_history.save()
            self.last_import_datetime = get_last_import_datetime(self.lock_name)
        if self.last_import_datetime:
            self.prepare_clause(self.last_import_datetime)
        return retval

    def _clean_up(self):
        self.dmis_import_history = None
        self.last_import_datetime = None,
        self.conditional_clause = None
        self.started = False
        self.lock = None
