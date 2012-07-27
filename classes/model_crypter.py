import sys
from django.db.models import get_models, get_app
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

from bhp_crypto.classes import BaseEncryptedField


class ModelCrypter(object):

    def encrypt_instance(self, instance, save=True):
        """ Encrypts the instance by calling save_base (not save!). """
        if save:
            instance.save_base(force_update=True, raw=True)
        return instance

    def get_encrypted_fields(self, model, **kwargs):
        """ Returns a list of field objects that use encryption.

        Keyword Arguments:
        field_name -- return a list with field object of this attname only
        """
        encrypted_fields = []
        field_name = kwargs.get('field_name', None)
        if field_name:
            encrypted_fields = [field for field in model._meta.fields if field.attname == field_name]
        for field in model._meta.fields:
            if isinstance(field, BaseEncryptedField):
                encrypted_fields.append(field)
        return encrypted_fields

    def get_encrypted_models(self, app_name, **kwargs):
        """ Returns a dictionary of model objects that contain encrypted fields.
        """
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
        """ Returns a dictionary of { app_name:  [encrypted_models, ...]}.
        """
        all_encrypted_models = {}
        for app_name in settings.INSTALLED_APPS:
            encrypted_models = self.get_encrypted_models(app_name)
            if encrypted_models:
                all_encrypted_models[app_name] = encrypted_models
        return all_encrypted_models

    def encrypt_model(self, model, save=True, **kwargs):
        """ Encrypts unencrypted instances for a given model.

        Keyword Arguments:
        print_on_save -- print a message to stdout on each save (default: True)
        save_message -- message to print after each instance is saved which
                        may include {0} and {1} for 'instance_count', 'instance_total'
                        (default: 37/35666 instances encrypted ...).
        field_name -- filter unencrypted instances on the field object with this attname only.
        """
        print_on_save = kwargs.get('print_on_save', True)
        save_message = kwargs.get('save_message', '\r\x1b[K {0} / {1} instances encrypted...')
        unencrypted_instances, field_name = self.get_unencrypted_instances(model, **kwargs)
        if not unencrypted_instances:
            instance_total = model.objects.all().count()
            if print_on_save:
                sys.stdout.write('{0} / {1} encrypted.\n'.format(instance_total, instance_total))
        else:
            instance_total = unencrypted_instances.count()
            instance_count = 0
            for unencrypted_instance in unencrypted_instances:
                instance_count += 1
                if save:
                    self.encrypt_instance(unencrypted_instance, save)
                if print_on_save:
                    if not save:
                        save_message = '{0} (not saved)'.format(save_message)
                    try:
                        sys.stdout.write(save_message.format(instance_count, instance_total))
                    except IndexError:
                        sys.stdout.write(save_message)
                    sys.stdout.flush()

    def decrypt_instance(self, instance,
                         encrypted_field_object=BaseEncryptedField):
        """ Returns a modified instance (not saved), encrypt all un-encrypted
        field objects in a given model instance.

        """
        for field in instance._meta.fields:
            if isinstance(field, BaseEncryptedField):
                setattr(instance, field.attname,
                        field.decrypt(getattr(instance, field.attname)))
        return instance

    def decrypt_model(self, model):
        """ decrypt and save all encrypted field objects in a given model """
        pass
        #for instance in model.objects.all():
        #    instance = self.decrypt_instance(self, instance,
        #                                      BaseEncryptedField)
        #    instance.save()

    def get_unencrypted_instances(self, model, **kwargs):
        """ Returns a tuple of (queryset, field_name) where queryset is
        instances selected by filtering on the field_name.

        Keyword Arguments:
        field_name -- filter on the field object with this attname only
                      (default: first field_name that filters for a queryset
                      with unencrypted instance)

        Note: If the instance is in an inconsistent state (not every field encrypted),
        this may not be accurate. Check the model after running once.
        """
        # check every encrypted field until you hit one
        field_name = kwargs.get('field_name', None)
        encrypted_fields = self.get_encrypted_fields(model, field_name=field_name)
        for encrypted_field in encrypted_fields:
            field_name = encrypted_field.attname
            field_startswith = '{0}__startswith'.format(encrypted_field.attname)
            encryption_prefix = encrypted_field.field_crypter.crypter.HASH_PREFIX
            unencrypted_instances = model.objects.exclude(**{field_startswith: encryption_prefix})
            if unencrypted_instances.count() > 0:
                return unencrypted_instances, field_name
        return model.objects.none(), field_name

    def is_instance_encrypted(self, **kwargs):
        """ Check if field values in instance are encrypted.

        Note: this is much slower than just saving the instance!!

        Keyword Arguments:
        instance -- a model instance (default: None)
        field_name -- filter on the field object with this attname only
        suppress_messages -- whether to print messages to stdout (default: False)

        """
        #suppress_messages = kwargs.get('suppress_messages', False)
        #field_name = kwargs.get('field_name', None)
        instance = kwargs.get('instance', None)
        if not instance:
            raise TypeError('Keyword argument \'instance\' cannot be None')
        return self._is_encrypted(**kwargs)

    def is_model_encrypted(self, **kwargs):
        """ Check if instances in model are encrypted.
        Note: this is much slower than just saving the instances!!

        Keyword Arguments:
        model -- checks all instances within model (default: None)
        field_name -- filter on the field object with this attname only
        suppress_messages -- whether to print messages to stdout (default: False)

        """
        #suppress_messages = kwargs.get('suppress_messages', False)
        #field_name = kwargs.get('field_name', None)
        model = kwargs.get('model', None)
        if not model:
            raise TypeError('Keyword argument \'model\' cannot be None')
        return self._is_encrypted(**kwargs)

    def _is_encrypted(self, **kwargs):
        """ Check if field values in instance/model are encrypted.
        Note: this is much slower than just saving the instance!!

        Keyword Arguments:
        instance -- limits the check to just this model instance (default: None)
        model -- checks all instances within model (default: None)
        field_name -- filter model or instance on the field object with this attname only
        suppress_messages -- whether to print messages to stdout (default: False)
        """
        instance = kwargs.get('instance', None)
        model = kwargs.get('model', None)
        field_name = kwargs.get('field_name', None)
        suppress_messages = kwargs.get('suppress_messages', False)
        model_name = model._meta.object_name.lower()
        if instance and model:
            raise TypeError('One of keyword arguments \'model\' and \instance\' must be None')
        if instance:
            model = instance.__class__
        else:
            try:
                instance = model.objects.all()[0]
            except:
                instance = None
        if not instance:
            is_encrypted = True
            if not suppress_messages:
                print ('(*) {model_name}. (empty!)').format(model_name=model_name,
                                                                         field_name=field_name)
        else:
            encrypted_fields = self.get_encrypted_fields(instance)
            if not encrypted_fields:
                if not suppress_messages:
                    print '{model_name} does not use field encryption.'.format(model_name=model_name)
                is_encrypted = None
            else:
                unencrypted_instances, field_name = self.get_unencrypted_instances(model, field_name=field_name)
                if unencrypted_instances.count() != 0:
                    is_encrypted = False
                    if not suppress_messages:
                        if unencrypted_instances.count() == model.objects.all().count():
                            if not suppress_messages:
                                print ('( ) {model_name}').format(model_name=model_name,
                                                                  field_name=field_name)
                        else:
                            print ('(?) {model_name}: {count} of {total} '
                                   'rows not encrypted').format(
                                        model_name=model_name,
                                        field_name=field_name,
                                        count=unencrypted_instances.count(),
                                        total=model.objects.all().count())
                elif model.objects.all().count() == 0:
                    is_encrypted = True
                    if not suppress_messages:
                        print ('(*) {model_name}. (empty!)').format(model_name=model_name,
                                                                                 field_name=field_name)
                else:
                    is_encrypted = True
                    if not suppress_messages:
                        print ('(*) {model_name}').format(model_name=model_name,
                                                          field_name=field_name)
        return is_encrypted
