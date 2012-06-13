from django.core.exceptions import ImproperlyConfigured
from bhp_crypto.classes import BaseEncryptedField


class StrongEncryptionField(BaseEncryptedField):
    
    def __init__(self, *args, **kwargs):
        
        # force the Crypter class to use of strong encryption
        if 'encryption_method' in kwargs:
            raise ImproperlyConfigured('StrongEncryptionField parameter \'encryption_method\' = \'strong\' by default.'  \
                                       ' Do not set this parameter at the model level.') 
        defaults = {'encryption_method': 'strong'}
        kwargs.update(defaults)
        
        super(StrongEncryptionField, self).__init__(*args, **kwargs)