import sys
import threading

from optparse import make_option
from django.core.management.base import BaseCommand  # CommandError
from bhp_crypto.classes import ModelCrypter


class Command(BaseCommand):

    args = '--model <model_name> --list --check'
    help = 'Encrypt fields within any INSTALLED_APP model using an encrypted field object.'
    option_list = BaseCommand.option_list + (
        make_option('--list',
            action='store_true',
            dest='list',
            default=False,
            help='List models using encryption. (list only, does not encrypt any data).'),
        )
    option_list += (
        make_option('--check',
            action='store_true',
            dest='check',
            default=False,
            help='Check if all fields models are encrypted. (checks only, does not encrypt any data).'),
        )
    option_list += (
        make_option('--model',
            action='store_true',
            dest='model',
            default=False,
            help='Check if all fields models are encrypted. (checks only, does not encrypt any data).'),
        )
    option_list += (
            make_option('--dry-run',
                action='store_true',
                dest='dry_run',
                default=False,
                help='Encrypt but do not save to the DB'),
            )

    def handle(self, *args, **options):

        self.save = True
        if options['dry_run']:
            self.save = False
        if options['list']:
            self._list_encrypted_models()
        elif options['check']:
            self._are_models_encrypted()
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

    def _encrypt_model(self, model, encrypted_fields):

        class CrypterThread(threading.Thread):
            def __init__(self, command, model_crypter, instance, encrypted_fields, instance_count, save):
                #print 'new thread {0}'.format(instance_count)
                self.model_crypter = model_crypter
                self.instance = instance
                self.encrypted_fields = encrypted_fields
                self.command = command
                self.save = save
                threading.Thread.__init__(self)

            def run(self):
                self.model_crypter.encrypt_instance(self.instance,
                                               self.encrypted_fields,
                                               save=self.save)
        n = 0
        model_crypter = ModelCrypter()
        try:
            app_name = model._meta.app_label
            model_name = model._meta.object_name.lower()
            self.stdout.write('Encrypting {app_name}.{model}...\n'.format(app_name=app_name,
                                                                          model=model_name))
            if not model_crypter.is_model_encrypted(model, suppress_messages=True):
                count = model.objects.all().count()
                instance_count = 0
                for instance in model.objects.all().order_by('id'):
                    instance_count += 1
                    maxconnections = 50
                    pool_sema = BoundedSemaphore(value=maxconnections)
                    pool_sema.acquire()
                    crypter_thread = CrypterThread(self, model_crypter, instance,
                                                   encrypted_fields, instance_count,
                                                   save=self.save)
                    crypter_thread.start()
                    pool_sema.release()
                    self.stdout.write('\r\x1b[K {0} / {1} instances '
                                          ' ...'.format(instance_count, count))
                    self.stdout.flush()
#                    model_crypter.encrypt_instance(instance, encrypted_fields, save=False)
#                    self.stdout.write('\r\x1b[K {0} / {1} instances '
#                                      ' ...'.format(instance_count, count))
#                    self.stdout.flush()
                self.stdout.write('done.\n')
                n += 1
                self.stdout.flush()
        except:
            raise
            #print "Unexpected error:", sys.exc_info()[0]
            #raise CommandError('Failed on {app_name}.{model}.{pk}.'.format(app_name=app_name,
            #                                                               model=model._meta.object_name.lower(),
            #                                                               pk=instance.pk))

    def _list_encrypted_models(self):
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
        self.stdout.write('{0} models use encryption.\n'.format(n))

    def _are_models_encrypted(self):
        model_crypter = ModelCrypter()
        all_encrypted_models = model_crypter.get_all_encrypted_models()
        for app_name, encrypted_models in all_encrypted_models.iteritems():
            print '\n' + app_name.upper()
            for meta in encrypted_models.itervalues():
                model = meta['model']
                model_crypter.is_model_encrypted(model)
