import sys
from optparse import make_option
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.db.models import get_models, get_app
from bhp_crypto.classes import BaseEncryptedField, ModelCrypter


class Command(BaseCommand):

    args = '--list'
    help = 'Encrypt fields within any INSTALLED_APP model using an encrypted field object.'
    option_list = BaseCommand.option_list + (
        make_option('--list',
            action='store_true',
            dest='list',
            default=False,
            help='List models using encryption. (list only, do not encrypt any data).'),
        )

    def handle(self, *args, **options):
        if options['list']:
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
        else:
            msg = 'No models to encrypt.'
            n = 0
            model_crypter = ModelCrypter()
            all_encrypted_models = model_crypter.get_all_encrypted_models()
            try:
                for app_name, encrypted_models in all_encrypted_models.iteritems():
                    for model_name, meta in encrypted_models.iteritems():
                        model = meta['model']
                        encrypted_fields = meta['encrypted_fields']
                        self.stdout.write('Encrypting {app_name}.{model}...\n'.format(app_name=app_name, model=model_name))
                        count = model.objects.all().count()
                        instance_count = 0
                        for instance in model.objects.all().order_by('id'):
                            instance_count += 1
                            model_crypter.encrypt_instance(instance, encrypted_fields, save=False)
                            self.stdout.write('\r\x1b[K {0} / {1} instances '
                                              ' ...'.format(instance_count, count))
                        self.stdout.write('done.\n')
                        n += 1
            except:
                print "Unexpected error:", sys.exc_info()[0]
                raise CommandError('Failed on {app_name}.{model}.{pk}.'.format(app_name=app_name,
                                                                               model=model._meta.object_name.lower(),
                                                                               pk=instance.pk))
            msg = 'Complete. {0} models encrypted.\n'.format(n)
            self.stdout.write(msg)
