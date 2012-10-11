from optparse import make_option
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from lab_import_lis.classes import LisLock, ImportHistory, Lis
from lab_clinic_api.classes import EdcLab


class Command(BaseCommand):

    args = (' --list-locks <lock_name> --unlock <lock_name> --import <subject_identifier>'
            '--show-history <lock_name>')
    help = 'Manage importing data from django-lis into your Edc using your \'lab_api\' database connection. '
    option_list = BaseCommand.option_list + (
        make_option('--list-locked',
            action='store_true',
            dest='list-locked',
            default=False,
            help=('List all locks.')),
         )
    option_list += (
        make_option('--unlock',
            action='store_true',
            dest='unlock',
            default=False,
            help=('Unlock for given lock name.')),
        )
    option_list += (
        make_option('--import',
            action='store_true',
            dest='import',
            default=False,
            help=('Initiate import of labs from django-lis into your Edc. '
                  'You may specify a subject_identifier to limit the import to just one subject. '
                  'Otherwise, the default is to import all for current protocol.')),
        )
    option_list += (
        make_option('--import-subject',
            action='store_true',
            dest='import_subject',
            default=False,
            help=('Initiate import of labs from django-lis into your Edc for one subject_identifier')),
        )
    option_list += (
        make_option('--show-history',
            action='store_true',
            dest='show_history',
            default=False,
            help=('Show history of data import for lock name.')),
        )

    def handle(self, *args, **options):
        #if not args:
        #    raise CommandError('Try --help for a list of valid options')
        db = 'lab_api'
        if not args:
            args = [None]
        lis_lock = LisLock(db)
        if options['list-locked']:
            for lock_name in args:
                self.list_locked(lis_lock, lock_name)
        elif options['unlock']:
            for lock_name in args:
                self.unlock(lis_lock, lock_name)
        elif options['import']:
            self.import_from_lis(db)
        elif options['import_subject']:
            if args:
                subject_identifier = args[0]
            else:
                raise CommandError('Please specify a subject_identifier')
            self.import_from_lis_for_subject(subject_identifier)
        elif options['show_history']:
            for lock_name in args:
                self.show_history(db, lis_lock, lock_name)
        else:
            raise CommandError('Unknown option, Try --help for a list of valid options')

    def import_from_lis(self, db, import_as_new=None):
        lis = Lis(db)
        lis.import_from_lis(protocol_identifier=settings.PROJECT_NUMBER)

    def import_from_lis_for_subject(self, subject_identifier):
        edc_lab = EdcLab()
        last_updated = edc_lab.update(subject_identifier)
        print last_updated

    def unlock(self, lis_lock, lock_name):
        if lock_name:
            lis_lock.release(lock_name)
        else:
            print 'Unable to released lock {0}. Try --list-locked for a list of valid locks.'.format(lock_name)

    def list_locked(self, lis_lock, lock_name):
        qs = lis_lock.list(lock_name)
        if qs:
            print 'Existing Locks:'
            for q in qs:
                print '  {0} {1}'.format(q.lock_name, q.created)
        else:
            print 'No locks exist for lock name \'{0}\'.'.format(lock_name)

    def show_history(self, db, lis_lock, lock_name):
        history = ImportHistory(db, lock_name).history()
        if not history:
            print 'No import history for lock name \'{0}\''.format(lock_name)
        else:
            print 'Import History:'
            print '  (lock name -- start -- finish)'
            for h in history:
                print '  {0} {1} {2}'.format(h.lock_name, h.start_datetime, h.end_datetime or 'Open')
        self.list_locked(lis_lock, lock_name)
