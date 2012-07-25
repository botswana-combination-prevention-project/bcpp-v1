from base_encrypted_field import BaseEncryptedField


class ModelCrypter(object):

    def encrypt_instance(self, instance, save=True):
        """ Returns a modified instance (not saved), encrypt all un-encrypted
        field objects in a given model instance. """
        for field in instance._meta.fields:
            if isinstance(field, BaseEncryptedField):
                field_value = getattr(instance, field.attname)
                if field_value:
                    if not field.is_encrypted(field_value):
                        setattr(instance, field.attname, field.encrypt(field_value))
                        if save:
                            instance.save()
        return instance

    def encrypt_model(self, model):
        """ Encrypt field objects that are an instance of BaseEncryptedField
        in a given model. """
        for instance in model.objects.all():
            instance = self.encrypt_instance(instance)

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
