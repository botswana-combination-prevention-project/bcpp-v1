from bhp_crypto.classes import BaseEncryptedField

class LocalRsaEncryptionField(BaseEncryptedField):
    
    """ Private key is expected to be available """
    
    def __init__(self, *args, **kwargs):
        
        self.algorithm='rsa'
        self.mode='local-rsa' 
        defaults = {'help_text': kwargs.get('help_text', '') + ' (Encryption: %s)' % (self.mode,) }
        kwargs.update(defaults)
        super(LocalRsaEncryptionField, self).__init__(*args, **kwargs)
        self.crypter.set_public_key(self.get_public_keyfile())
        self.crypter.set_private_key(self.get_private_keyfile())
        if not self.crypter.private_key:
            print 'warning: {0} key {1} not found'.format(self.mode, self.get_private_keyfile())

        