from django.core.management.base import BaseCommand
from bhp_crypto.classes import Crypter
from bhp_sync.models import OutgoingTransaction, IncomingTransaction


class Command(BaseCommand):
    args = '--list'
    help = 'Encrypt Incoming and outgoing transactions.'

    def handle(self, *args, **options):
        crypter = Crypter()
        crypter.algorithm = 'aes'
        crypter.mode = 'aes-local'
        count = OutgoingTransaction.objects.all().count()
        instance_count = 0
        self.stdout.writeln('{} Outgoing transactions found'.format(count))
        for transaction in OutgoingTransaction.objects.all():
            instance_count += 1
            if not "enc:::" in transaction.tx:
                transaction.tx = crypter.encrypt(transaction.tx)
                transaction.save()
                self.stdout.write('\r\x1b[K {0} / {1} transactions '
                                  ' ...'.format(instance_count, count))
        self.stdout.write('done.\n')
