from optparse import make_option
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from bhp_sync.classes import SyncLock, ImportHistory, Consumer
from bhp_lab_tracker.classes import site_lab_tracker

site_lab_tracker.autodiscover()


class Command(BaseCommand):

    args = ('--consume --list-locked --unlock --copy_from_server')
    help = 'Consume incoming transactions already fetched from producers. '
    option_list = BaseCommand.option_list + (
        make_option('--list-locked',
            action='store_true',
            dest='list-locked',
            default=False,
            help=('Show lock.')),
         )
    option_list += (
        make_option('--unlock',
            action='store_true',
            dest='unlock',
            default=False,
            help=('Unlock.')),
        )
    option_list += (
        make_option('--show-history',
            action='store_true',
            dest='show_history',
            default=False,
            help=('Show history of data import for lock name.')),
        )
    option_list += (
        make_option('--consume',
            action='store_true',
            dest='consume',
            default=False,
            help=('Show history of data import for lock name.')),
        )
    option_list += (
        make_option('--copy_from_server',
            action='store_true',
            dest='copy_from_server',
            default=False,
            help=('Copy unconsumed incoming transactions from server to your local installation.')),
        )

    def get_consumer(self):
        """Returns the consumer class instances.

        Users should override to provide an app specific consumer."""
        return Consumer()

    def handle(self, *args, **options):
        db = 'default'
        settings.APP_NAME
        lock_name = 'consume-{0}'.format(settings.APP_NAME)
        if not args:
            args = [None]
        sync_lock = SyncLock(db)
        if options['consume']:
            self.consume(lock_name)
        #elif options['copy_from_server']:
        #    self.copy_from_server()
        elif options['list-locked']:
            for lock_name in args:
                self.list_locked(sync_lock, lock_name)
        elif options['unlock']:
            for lock_name in args:
                self.unlock(sync_lock, lock_name)
        elif options['show_history']:
            for lock_name in args:
                self.show_history(db, sync_lock, lock_name)
        else:
            raise CommandError('Unknown option, Try --help for a list of valid options')

    def consume(self, lock_name):
        consumer = self.get_consumer()
        consumer.consume(lock_name=lock_name)

    def copy_from_server(self):
        raise CommandError('Option not available')
        #consumer = Consumer()
        #consumer.copy_incoming_from_server()

    def unlock(self, sync_lock, lock_name):
        if lock_name:
            sync_lock.release(lock_name)
        else:
            print 'Unable to released lock {0}. Try --list-locked for a list of valid locks.'.format(lock_name)

    def list_locked(self, sync_lock, lock_name):
        qs = sync_lock.list(lock_name)
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
