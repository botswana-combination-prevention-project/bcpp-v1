from bhp_crypto.classes import BaseEncryptedField
from django.core.exceptions import ImproperlyConfigured


class WeakEncryptionField(BaseEncryptedField):
    
    def __init__(self, *args, **kwargs):
        
        # force the Crypter class to use of strong encryption
        if 'encryption_method' in kwargs:
            raise ImproperlyConfigured('WeakEncryptionField parameter \'encryption_method\' = \'weak\' by default.'  \
                                       ' Do not set this parameter at the model level.') 
        defaults = {'encryption_method': 'weak'}
        kwargs.update(defaults)
        
        super(WeakEncryptionField, self).__init__(*args, **kwargs)