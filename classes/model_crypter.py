from django.db.models import get_models, get_app
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

from bhp_crypto.classes import BaseEncryptedField


class ModelCrypter(object):

    def encrypt_instance(self, instance, encrypted_fields=None, save=True):
        """ Returns a modified instance (not saved), encrypt all un-encrypted
        field objects in a given model instance. """
        if not encrypted_fields:
            encrypted_fields = self.get_encrypted_fields(instance)
        for field in encrypted_fields:
            field_value = getattr(instance, field.attname)
            if field_value:
                if not field.is_encrypted(field_value):
                    setattr(instance, field.attname, field.encrypt(field_value))
                    if save:
                        instance.save()
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
