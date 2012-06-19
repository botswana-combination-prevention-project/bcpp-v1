from django.db.models import get_models
from crypter import Crypter
from bhp_crypto.classes import BaseEncryptedField


class AlreadyRegistered(Exception):
    pass

class NotRegistered(Exception):
    pass       

class CryptoModelController(object):
    
    crypter = Crypter()
    
    def __init__(self):
        self._registry = []
        
    def register(self, model):  
        """ register all models that use an encrypted field """
        if model in self._registry:
            raise AlreadyRegistered('The model %s is already registered' % model.__name__)
        else:
            self._registry.append(model)

    def autodiscover(self):
        
        for model in get_models():
            for field in model._meta.fields:
                if isinstance(field, BaseEncryptedField):
                    self.register(model)
                    break
                
crypto_models = CryptoModelController()
