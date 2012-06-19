from django.conf import settings
from django import forms
from django.core.exceptions import ImproperlyConfigured
from bhp_crypto.classes import BaseEncryptedField


class RestrictedKeyPairEncryptionField(BaseEncryptedField):
    
    """ Encrypts using a key pair but will raise an error if the private key is available and IS_SECURE_DEVICE is False. """
    
    def __init__(self, *args, **kwargs):
        
        self.algorithm = 'RSA'
        self.mode = 'restricted key-pair'
        # will force the Crypter class to use restricted key-pair encryption
        # so the model field attribute should not be specified        
        if 'encryption_method' in kwargs:
            raise ImproperlyConfigured('RestrictedKeyPairEncryptionField parameter \'encryption_method\' = \'%s\' by default.'  \
                                       ' Do not set this parameter at the model level.' % (self.mode,)) 
        defaults = {'encryption_method': self.mode,
                    'help_text': kwargs.get('help_text', '') + ' (Encryption: %s)' % (self.mode,),}
        kwargs.update(defaults)
        
        # we need this settings attribute when determining if the private key may be available
        if not hasattr(settings, 'IS_SECURE_DEVICE'):
            raise ImproperlyConfigured('You must set the IS_SECURE_DEVICE setting to True ' \
                                       'or False for \'restricted key-pair\' encryption' )
        super(RestrictedKeyPairEncryptionField, self).__init__(*args, **kwargs)
        
    def get_public_keyfile(self):
        self.public_keyfile = None
        if not hasattr(settings, 'PUBLIC_KEY_RESTRICTED'):
            raise ImproperlyConfigured('For \'%s\' security, you must set the PUBLIC_KEY_RESTRICTED setting to ' \
                                        'point to your public key (path and filename).' % (self.mode,))
        return settings.PUBLIC_KEY_RESTRICTED  

    def get_private_keyfile(self): 
        retval = None
        if 'PRIVATE_KEY_RESTRICTED' in dir(settings):
            # restricted key-pair security DOES NOT expect a private key to be available on an insecure device
            if settings.PRIVATE_KEY_RESTRICTED:
                if not 'IS_SECURE_DEVICE' in dir(settings):
                    raise ImproperlyConfigured('For \'%s\' security, set the IS_SECURE_DEVICE setting to ' \
                                        'True (secure) or False (insecure).' % (self.mode,))    
                if not settings.IS_SECURE_DEVICE == True:
                    raise ImproperlyConfigured('PRIVATE_KEY_RESTRICTED setting should not be available on a insecure device.' )
                retval = settings.PRIVATE_KEY_RESTRICTED  
        return retval
     
    #    def formfield(self, **kwargs):
    #        # This is a fairly standard way to set up some defaults
    #        # while letting the caller override them 
    #        defaults = {'widget': forms.widgets.TextInput(render_value=True)}
    #        defaults.update(kwargs)
    #        return super(RestrictedKeyPairEncryptionField, self).formfield(**defaults)                  
        