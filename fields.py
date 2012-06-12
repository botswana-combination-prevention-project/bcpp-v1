"""
Erik's additional encrypted model fields, try one!
"""
from classes import BaseEncryptedField
from django.core.exceptions import ImproperlyConfigured

class StrongEncryptionField(BaseEncryptedField):
    
    def __init__(self, *args, **kwargs):
        
        # force the Crypter class to use of strong encryption
        if 'encryption_method' in kwargs:
            raise ImproperlyConfigured('StrongEncryptionField parameter \'encryption_method\' = \'strong\' by default.'  \
                                       ' Do not set this parameter at the model level.') 
        defaults = {'encryption_method': 'strong'}
        kwargs.update(defaults)
        
        super(StrongEncryptionField, self).__init__(*args, **kwargs)


class WeakEncryptionField(BaseEncryptedField):
    
    def __init__(self, *args, **kwargs):
        
        # force the Crypter class to use of strong encryption
        if 'encryption_method' in kwargs:
            raise ImproperlyConfigured('WeakEncryptionField parameter \'encryption_method\' = \'weak\' by default.'  \
                                       ' Do not set this parameter at the model level.') 
        defaults = {'encryption_method': 'weak'}
        kwargs.update(defaults)
        
        super(WeakEncryptionField, self).__init__(*args, **kwargs)
        
        
class EncryptedIdentityField(StrongEncryptionField):
    def __init__(self, *args, **kwargs):
        super(EncryptedIdentityField, self).__init__(*args, **kwargs)


class EncryptedFirstnameField(WeakEncryptionField):
    pass

class EncryptedLastnameField(StrongEncryptionField):
    pass