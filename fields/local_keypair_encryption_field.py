from django.conf import settings
from bhp_crypto.classes import BaseEncryptedField
from django.core.exceptions import ImproperlyConfigured


class LocalKeyPairEncryptionField(BaseEncryptedField):
    
    """  'local key-pair': same as 'restricted key-pair' but the private key is expected to be available and it's absence is not enforced """

    def __init__(self, *args, **kwargs):
        
        if not 'algorithm' in dir(self):
            raise TypeError('Algorithm may not be None or unset. Set to RSA or AES in the subclass')
        if not self.algorithm:
            raise TypeError('Algorithm may not be None. Set to RSA or AES in the subclass')
        super(LocalKeyPairEncryptionField, self).__init__(*args, **kwargs)
    
    def get_public_keyfile(self):
        if not hasattr(settings, 'PUBLIC_KEY_LOCAL'):
            raise ImproperlyConfigured('For \'%s\' security, you must set the PUBLIC_KEY_LOCAL setting to ' \
                                        'point to your public key (path and filename) .' % (self.mode,))
        return settings.PUBLIC_KEY_LOCAL 

    def get_private_keyfile(self):
        retval = None
        if 'PRIVATE_KEY_LOCAL' in dir(settings):
            # medium security expects a private key to be available on the device, 
            # but you could remove move it to fully de-identify the DB
            if settings.PRIVATE_KEY_LOCAL:
                retval = settings.PRIVATE_KEY_LOCAL
        return retval 
    
    #    def formfield(self, **kwargs):
    #        # This is a fairly standard way to set up some defaults
    #        # while letting the caller override them 
    #        defaults = {'widget': forms.widgets.PasswordInput(render_value=True)}
    #        defaults.update(kwargs)
    #        return super(WeakEncryptionField, self).formfield(**defaults)        
