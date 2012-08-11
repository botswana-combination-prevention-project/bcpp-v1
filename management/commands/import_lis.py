from optparse import make_option
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from lab_clinic_api.classes import LisLock, ImportHistory, Lis


class Command(BaseCommand):

    args = (' --list-locks <lock_name> --unlock <lock_name> --import '
            '--show-history <lock_name>')
    help = 'Manage django-lis import.'
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
            help=('Initiate import of labs from django-lis into django-edc.')),
        )
#    option_list += (
#        make_option('--import_as_new',
#            action='store_true',
#            dest='import_as_new',
##            default=False,
##            help=('Initiate import of labs from dmis into django-lis. '
#                  'Force listed models to be recreated')),
#        )
    option_list += (
        make_option('--show-history',
            action='store_true',
            dest='show_history',
            default=False,
            help=('Show history of data import for lock name.')),
        )

    def handle(self, *args, **options):
        if not args:
            raise CommandError('Try --help for a list of valid options')
        #args = list(args)
        #db = args.pop(0)
        #if not db:
        #    raise CommandError('Missing argument \'db\', Try --help for a list of valid arguments and options')
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
        elif options['show_history']:
            for lock_name in args:
                self.show_history(db, lis_lock, lock_name)
        else:
            raise CommandError('Unknown option, Try --help for a list of valid options')

    def import_from_lis(self, db, import_as_new=None):
        lis = Lis(db)
        lis.import_from_lis(protocol_identifier=settings.PROJECT_NUMBER)

    def unlock(self, lis_lock, lock_name):
        if lock_name:
            lis_lock.release(lock_name)
        else:
            print 'Unable to released lock {0}. Try --list for a list of valid locks.'.format(lock_name)

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
