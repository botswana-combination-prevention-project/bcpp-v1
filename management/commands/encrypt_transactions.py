from django.core.management.base import BaseCommand, CommandError
from bhp_crypto.classes import Crypter
from django.db.models import get_model


class Command(BaseCommand):
    args = '<model_name>'
    help = 'Encrypt Incoming and outgoing transactions.'

    def handle(self, *args, **options):
        crypter = Crypter()
        crypter.algorithm = 'aes'
        crypter.mode = 'aes-local'
        model = None
        if not args:
            self.stdout.write('Encrypting both incoming and outgoing.\n')
            self.stdout.write('Starting with incoming.\n')
            self.encrypt_tx(crypter, get_model('bhp_sync', 'incomingtransaction'))

            self.stdout.write('Processing with outgoing.\n')
            self.encrypt_tx(crypter, get_model('bhp_sync', 'outgoingtransaction'))
        else:
            for model_name in args:
                if model_name.lower() == 'outgoing':
                    model = get_model('bhp_sync', 'outgoingtransaction')
                elif model_name.lower() == 'incoming':
                    model = get_model('bhp_sync', 'incomingtransaction')
                else:
                    raise CommandError('Model {} not found'.format(model_name))
            if model:
                self.encrypt_tx(crypter, model)

    def encrypt_tx(self, crypter, model):
        count = model.objects.all().count()
        instance_count = 0
        already_enc_count = 0
        self.stdout.write('{0} {1} transactions found.\n'.format(model.__name__,count))
        for transaction in model.objects.all():
            instance_count += 1
            tx = str(transaction.tx)
            if not "enc1:::" in tx:
                transaction.tx = crypter.encrypt(transaction.tx)
                transaction.save()

            else:
                already_enc_count += 1

            self.stdout.write('\r\x1b[K {0} / {1} transactions: already encrypted {2} / {1}'
                                  ' ...'.format(instance_count, count, already_enc_count))
            self.stdout.flush()

        self.stdout.write('done.\n')
