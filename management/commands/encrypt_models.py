from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.db.models import get_models, get_app
from bhp_crypto.classes import BaseEncryptedField, ModelCrypter


class Command(BaseCommand):
    #args = '<poll_id poll_id ...>'
    help = 'Encrypt fields within any INSTALLED_APP model using an encrypted field object.'

    def handle(self, *args, **options):

        msg = 'No models to encrypt.'
        n = 0
        for app_name in settings.INSTALLED_APPS:
            try:
                app = get_app(app_name)
            except:
                app = None
            if app:
                # self.stdout.write(app_name + '\n')
                for model in get_models(app):
                    # self.stdout.write(model._meta.object_name + '\n')
                    for field in model._meta.fields:
                        if isinstance(field, BaseEncryptedField):
                            if not field.crypter.has_encryption_key:
                                raise CommandError('Suspect encryption keys are not loaded. Quitting.')
                            self.stdout.write('Encrypting {app_name}.{model}...\n'.format(app_name=app_name, model=model._meta.object_name.lower()))
                            model_crypter = ModelCrypter()
                            count = model.objects.all().count()
                            instance_count = 0
                            try:
                                for instance in model.objects.all():
                                    instance_count += 1
                                    instance = model_crypter.encrypt_instance(instance)
                                    instance.save()
                                    self.stdout.write("\r\x1b[K" + '{0} / {1} instances ...'.format(instance_count, count))
                                self.stdout.write('done.\n')
                                n += 1
                                break
                            except:
                                raise CommandError('Failed on {app_name}.{model}.{pk}.'.format(app_name=app_name,
                                                                                            model=model._meta.object_name.lower(),
                                                                                            pk=model.pk))
                msg = 'Complete. {0} models encrypted.\n'.format(n)
        self.stdout.write(msg)
