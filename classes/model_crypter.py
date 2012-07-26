from django.db.models import get_models, get_app
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

from bhp_crypto.classes import BaseEncryptedField


class ModelCrypter(object):

    def encrypt_instance(self, instance, encrypted_fields=None, save=True):
        """ Returns a modified instance (not saved), encrypt all un-encrypted
        field objects in a given model instance. """
        #if not encrypted_fields:
        #    encrypted_fields = self.get_encrypted_fields(instance)
        #for field in encrypted_fields:
        #    field_value = getattr(instance, field.attname)
        #    if field_value:
        #        if not field.is_encrypted(field_value):
        #            encrypted_field_value = field.encrypt(field_value)
        #            setattr(instance, field.attname, encrypted_field_value)
        if save:
            instance.save()
            # instance.save_base(force_update=True, raw=True)
        return instance

    def get_encrypted_fields(self, model):
        """ Returns a list of encrypted field objects """
        encrypted_fields = []
        for field in model._meta.fields:
            if isinstance(field, BaseEncryptedField):
                encrypted_fields.append(field)
        return encrypted_fields

    def get_encrypted_models(self, app_name):
        """ Returns a list of model objects that contain encrypted fields """
        encrypted_models = {}
        try:
            app = get_app(app_name)
        except ImproperlyConfigured:
            app = None
            pass
        if app:
            for model in get_models(get_app(app_name)):
                encrypted_fields = self.get_encrypted_fields(model)
                if encrypted_fields:
                    encrypted_models[model._meta.object_name.lower()] = {'model': model, 'encrypted_fields': encrypted_fields}
        return encrypted_models

    def get_all_encrypted_models(self):
        """ Returns a dictionary of { app_name:  [encrypted_models, ...]} """
        all_encrypted_models = {}
        for app_name in settings.INSTALLED_APPS:
            encrypted_models = self.get_encrypted_models(app_name)
            if encrypted_models:
                all_encrypted_models[app_name] = encrypted_models
        return all_encrypted_models

    def encrypt_model(self, model):
        """ Encrypts field objects that are an instance of BaseEncryptedField
        in a given model. """
        encrypted_fields = []
        for field in model._meta.fields:
            if isinstance(field, BaseEncryptedField):
                encrypted_fields.append(field)
        for instance in model.objects.all():
            instance = self.encrypt_instance(instance, encrypted_fields)

    def decrypt_instance(self, instance,
                         encrypted_field_object=BaseEncryptedField):
        """ Returns a modified instance (not saved), encrypt all un-encrypted
        field objects in a given model instance. """
        for field in instance._meta.fields:
            if isinstance(field, BaseEncryptedField):
                setattr(instance, field.attname,
                        field.decrypt(getattr(instance, field.attname)))
        return instance

    def decrypt_model(self, model):
        """ decrypt and save all encrypted field objects in a given model """
        for instance in model.objects.all():
            instance = self.decrypt_instance(self, instance,
                                              BaseEncryptedField)
            instance.save()

    def is_model_encrypted(self, model, suppress_messages=False):
        encrypted_fields = self.get_encrypted_fields(model)
        is_encrypted = True
        if not encrypted_fields:
            print '{model_name} does not use field encryption.'.format(model_name=model._meta.object_name.lower())
            is_encrypted = None
        else:
            for encrypted_field in encrypted_fields:
                field_startswith = '{0}__startswith'.format(encrypted_field.attname)
                this_value = encrypted_field.field_crypter.crypter.HASH_PREFIX
                if model.objects.exclude(**{field_startswith: this_value}).count() != 0:
                    if model.objects.exclude(**{field_startswith: this_value}).count() != model.objects.all().count():
                        if not suppress_messages:
                            print ('(?) {model_name}.{field_name}: {count} of {total} '
                                   'rows not encrypted').format(model_name=model._meta.object_name.lower(),
                                                                field_name=encrypted_field.attname,
                                                                count=model.objects.exclude(**{field_startswith: this_value}).count(),
                                                                total=model.objects.all().count())
                    else:
                        if not suppress_messages:
                            print ('( ) {model_name}.{field_name}').format(model_name=model._meta.object_name.lower(),
                                                                            field_name=encrypted_field.attname,)
                    is_encrypted = False
                elif model.objects.all().count() == 0:
                    if not suppress_messages:
                        print ('( ) {model_name}.{field_name}. (empty)').format(model_name=model._meta.object_name.lower(),
                                                                            field_name=encrypted_field.attname,)
                else:
                    if not suppress_messages:
                        print ('(*) {model_name}.{field_name}').format(model_name=model._meta.object_name.lower(),
                                                                       field_name=encrypted_field.attname,)
                    #else:
                    #    print '{model_name} is already encrypted'.format(model_name=model._meta.object_name.lower())
        if is_encrypted:
            print ' {model_name} is already encrypted or empty'.format(model_name=model._meta.object_name.lower())
        return is_encrypted
