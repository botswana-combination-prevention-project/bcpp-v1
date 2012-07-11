from base_encrypted_field import BaseEncryptedField

class ModelCrypter(object):
    
    def encrypt_instance(self, instance):
        """ returns a modified instance (not saved), encrypt all un-encrypted field objects in a given model instance """
        for field in instance._meta.fields:
            if isinstance(field, BaseEncryptedField):
                try:
                    setattr(instance, field.attname, field.encrypt(getattr(instance, field.attname)))
                except:
                    pass
        return instance        
    
    def encrypt_model(self, model):
        """ encrypt field objects that are an instance of BaseEncryptedField in a given model """
        for instance in model.objects.all():
            instance  = self.encrypt_instance(instance)
            instance.save()
                
    def decrypt_instance(self, instance, encrypted_field_object=BaseEncryptedField):
        """ returns a modified instance (not saved), encrypt all un-encrypted field objects in a given model instance """
        for field in instance._meta.fields:
            if isinstance(field, BaseEncryptedField):
                setattr(instance, field.attname, field.decrypt(getattr(instance, field.attname)))
        return instance        
     
    def decrypt_model(self, model):
        """ decrypt and save all encrypted field objects in a given model """
        for instance in model.objects.all():
            instance  = self.decrypt_instance(self, instance, BaseEncryptedField)
            instance.save()
            
            