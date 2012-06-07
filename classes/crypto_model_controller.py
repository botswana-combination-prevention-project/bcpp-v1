#
#import copy
#from django.conf import settings
#from django.utils.importlib import import_module
#from django.utils.module_loading import module_has_submodule
#from crypter import Crypter
#from base_encrypted_field import BaseEncryptedField
#from bhp_crypto.models import Crypt
#
#
#class AlreadyRegistered(Exception):
#    pass
#
#class NotRegistered(Exception):
#    pass       
#
#class CryptoModelController(object):
#    
#    crypter = Crypter()
#    
#    def __init__(self):
#        # contains model_cryptos {model:model_crypto}
#        self._registry = []
#        
#    def register(self, model):  
#        """ """
#        if model in self._registry:
#            raise AlreadyRegistered('The model %s is already registered' % model.__name__)
#        self._registry.append(model)
#              
#    def update(self, instance):
#        
#        """ during pre_save, given a model instance, review fields to find encrypted_fields and process.
#        1. truncate the instance encrypted field value to just prefix + hash  
#        2. save hash, cipher pair to crypt model """    
#        
#        for model in self._registry:
#            if isinstance(instance,model):
#                for field in model._meta.fields:
#                    if isinstance(field, BaseEncryptedField):
#                        # get hash and cipher before changing the instance field value
#                        value = getattr(instance, field.name)
#                        hash_text = self.crypter.get_hash(value)
#                        cipher_text = self.crypter.get_cipher(value)
#                        # set / change instance field value to be just the prefix + hash (truncate off the cipher)
#                        # just want to store hash to maintain a meaningful unique constraint
#                        setattr(instance, field.name, self.crypter.prefix + hash_text)
#                        self.update_crypt_model(hash_text, cipher_text)
#                        
#    def update_reference_model(self, hash_text, cipher_text):
#        """ update a model to have a reference of hash_value / cipher_value pairs """
#        # get and update or create the crypt model with this hash, cipher pair
#        if Crypt.objects.filter(hash_text=hash_text):
#            if cipher_text:
#                crypt = Crypt.objects.get(hash_text=hash_text)
#                crypt.cipher_text = cipher_text
#                crypt.save()
#        else:
#            if cipher_text:
#                Crypt.objects.create(hash_text=hash_text, cipher_text=cipher_text)
#            else:
#                # if the hash is not in the crypt model and you do not have a cipher
#                # this is an error condition
#                raise TypeError('Expected cipher text for given new hash, but got None.')
#    
#    def autodiscover(self):
#        
#        for app in settings.INSTALLED_APPS:
#            mod = import_module(app)
#            try:
#                before_import_registry = copy.copy(crypto_models._registry)
#                import_module('%s.crypto_models' % app)
#            except:
#                crypto_models._registry = before_import_registry
#                if module_has_submodule(mod, 'crypto_models'):
#                    raise
#        
#crypto_models = CryptoModelController()
#        