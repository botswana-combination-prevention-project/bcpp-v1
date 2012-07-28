#import sys
#import threading

from optparse import make_option
from django.core.management.base import BaseCommand  # CommandError
from bhp_crypto.classes import ModelCrypter, FieldCrypter
from bhp_crypto.models import Crypt


class Command(BaseCommand):

    args = '--list-models --list-fields --check --dry-run'
    help = 'Encrypt fields within any INSTALLED_APP model using an encrypted field object.'
    option_list = BaseCommand.option_list + (
        make_option('--list-models',
            action='store_true',
            dest='list',
            default=False,
            help='Lists models using encryption. (Safe. Lists only, does not encrypt any data).'),
        )
    option_list += (
        make_option('--check',
            action='store_true',
            dest='check',
            default=False,
            help='Checks if all instances of each model are encrypted. (checks only, does not encrypt any data).'),
        )
    option_list += (
        make_option('--list-fields',
            action='store_true',
            dest='list_fields',
            default=False,
            help='Lists the fields in each model using encryption. (Safe. Lists only, does not encrypt any data)..'),
        )
    option_list += (
            make_option('--dry-run',
                action='store_true',
                dest='dry_run',
                default=False,
                help='Encrypts without saving. (Safe. Does not encrypt any data)'),
            )
    option_list += (
            make_option('--verify-lookup',
                action='store_true',
                dest='dry_run',
                default=False,
                help='Verify secrets and hashing in lookup table, bhp_crypto.models.crypt. (Safe. Does not encrypt any data)'),
            )

    def handle(self, *args, **options):

        self.save = True
        if options['dry_run']:
            self.save = False
        if options['list']:
            self._list_encrypted_models()
        elif options['check']:
            self._check_models_encrypted()
        elif options['list_fields']:
            self._list_encrypted_fields()
        else:
            msg = 'No models to encrypt.'
            n = 0
            model_crypter = ModelCrypter()
            all_encrypted_models = model_crypter.get_all_encrypted_models()
            if all_encrypted_models:
                for encrypted_models in all_encrypted_models.itervalues():
                    for meta in encrypted_models.itervalues():
                        model = meta['model']
                        encrypted_fields = meta['encrypted_fields']
                        self._encrypt_model(model, encrypted_fields)
                msg = 'Complete. {0} models encrypted.\n'.format(n)
            self.stdout.write(msg)

    def _encrypt_model(self, model, save=True):
        """ Encrypts all unencrypted instances for given model.

        You may need to run this more than once if any instances
        are partially encrypted"""
        model_crypter = ModelCrypter()
        app_name = model._meta.app_label
        model_name = model._meta.object_name.lower()
        self.stdout.write('Encrypting {app_name}.{model}...\n'.format(app_name=app_name,
                                                                      model=model_name))
        model_crypter.encrypt_model(model, save)
        self.stdout.write('done.\n')
        self.stdout.flush()

    def _list_encrypted_models(self, list_fields=False):
        model_crypter = ModelCrypter()
        n = 0
        all_encrypted_models = model_crypter.get_all_encrypted_models()
        for app_name, encrypted_models in all_encrypted_models.iteritems():
            for meta in encrypted_models.itervalues():
                model = meta['model']
                encrypted_fields = meta['encrypted_fields']
                n += 1
                self.stdout.write('{app_name}.{model}. {encrypted_fields} '
                                  'fields.\n'.format(app_name=app_name,
                                                     model=model._meta.object_name.lower(),
                                                     encrypted_fields=len(encrypted_fields)))
                if list_fields:
                    self.stdout.write('  {encrypted_fields}\n'.format(encrypted_fields=' \n  '.join(([' '.join((field.attname, '-'.join((field.algorithm, field.mode)))) for field in encrypted_fields]))))

        self.stdout.write('{0} models use encryption.\n'.format(n))

    def _list_encrypted_fields(self):
            self._list_encrypted_models(True)

    def _check_models_encrypted(self):
        model_crypter = ModelCrypter()
        all_encrypted_models = model_crypter.get_all_encrypted_models()
        for app_name, encrypted_models in all_encrypted_models.iteritems():
            print '\n' + app_name.upper()
            for meta in encrypted_models.itervalues():
                model = meta['model']
                model_crypter.is_model_encrypted(model=model)

    def verify_secrets(self, *args, **options):
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
