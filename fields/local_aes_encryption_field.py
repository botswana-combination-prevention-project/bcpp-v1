from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
#from django.forms import widgets
from local_keypair_encryption_field import LocalKeyPairEncryptionField
#from bhp_base_model.widgets import ReadOnlyWidget

class LocalAesEncryptionField(LocalKeyPairEncryptionField):
    
    def __init__(self, *args, **kwargs):
        
        self.algorithm = 'AES'

        self.mode = 'local AES'
        
        # will force the Crypter class to use 'local key-pair' encryption
        # so the model field attribute should not be specified
        if 'encryption_method' in kwargs:
            raise ImproperlyConfigured('LocalKeyPairEncryptionField parameter \'encryption_method\' = \'%s\' by default.'  \
                                       ' Do not set this parameter as model field attribute.' % (self.mode,)) 
        defaults = {'encryption_method': self.mode,
                    'help_text': kwargs.get('help_text', '') + ' (Encryption: {0})'.format(self.mode,) }
        kwargs.update(defaults)
        super(LocalAesEncryptionField, self).__init__(*args, **kwargs)        


    def get_aes_key(self):
        retval = None
        if 'AES_KEY' in dir(settings):
            if settings.AES_KEY:
                retval = settings.AES_KEY
        return retval 
    
        