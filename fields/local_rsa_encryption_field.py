from django.core.exceptions import ImproperlyConfigured
from local_keypair_encryption_field import LocalKeyPairEncryptionField


class LocalRsaEncryptionField(LocalKeyPairEncryptionField):
    
    """  'local RSA key-pair': same as 'restricted key-pair' but the private key is expected to be available and it's absence is not enforced """
    
    def __init__(self, *args, **kwargs):
        
        self.algorithm='rsa'
        self.mode='local-rsa'
        # will force the Crypter class to use 'local key-pair' encryption
        # so the model field attribute should not be specified
        if 'encryption_method' in kwargs:
            raise ImproperlyConfigured('LocalKeyPairEncryptionField parameter \'encryption_method\' = \'%s\' by default.'  \
                                       ' Do not set this parameter as model field attribute.' % (self.mode,)) 
        defaults = {'encryption_method': self.mode,
                    'help_text': kwargs.get('help_text', '') + ' (Encryption: %s)' % (self.mode,) }
        kwargs.update(defaults)
        super(LocalRsaEncryptionField, self).__init__(*args, **kwargs)