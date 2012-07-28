from django.core.management.base import BaseCommand
from bhp_crypto.classes import FieldCrypter
from bhp_crypto.models import Crypt


class Command(BaseCommand):
    help = 'Verify secrets and hashes stored in lookup model (bhp_crypto.models.crypt)'

    def handle(self, *args, **options):
        self.stdout.write('Verify secrets and hashes stored in lookup model '
                          '(bhp_crypto.models.crypt)...\n')
        self.stdout.write('Verify from newest to oldest.\n')
        n = 0
        verified = 0
        failed_hash = 0
        failed_decrypt = 0
        total = Crypt.objects.all().count()
        for instance in Crypt.objects.all().order_by('-modified'):
            self.stdout.write('\r\x1b[K {0} / {1} verifying...'.format(n, total))
            n += 1
            field_crypter = FieldCrypter(instance.algorithm, instance.mode)
            try:
                plain_text = field_crypter.decrypt(field_crypter.crypter.HASH_PREFIX +
                                                   instance.hash +
                                                   field_crypter.crypter.SECRET_PREFIX +
                                                   instance.secret)
                test_hash = field_crypter.get_hash(plain_text)
                if test_hash != instance.hash:
                    failed_hash += 1
                    self.stdout.write('pk=\'{0}\' failed on hash comparison\n'.format(instance.id))
                else:
                    verified += 1
            except:
                self.stdout.write('pk=\'{0}\' failed on decrypt\n'.format(instance.id))
                failed_decrypt += 1
            del field_crypter
            self.stdout.flush()
        self.stdout.write(('Total: {0}\nVerified: {1}\nFailed decrypt: {2}\nFailed decrypt: '
                          ' {3}\nDone.').format(n, verified, failed_decrypt, failed_hash))
