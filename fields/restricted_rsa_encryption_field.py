from restricted_keypair_encryption_field import RestrictedKeyPairEncryptionField


class RestrictedRsaEncryptionField(RestrictedKeyPairEncryptionField):
    
    """  'local RSA key-pair': same as 'restricted key-pair' but the private key is expected to be available and it's absence is not enforced """
    
    def __init__(self, *args, **kwargs):
        
        self.algorithm='rsa'
        self.mode='restricted-rsa'
        defaults={'encryption_method': self.mode,
                  'help_text': kwargs.get('help_text', '')+' (Encryption: %s)' % (self.mode,) }
        kwargs.update(defaults)
        super(RestrictedRsaEncryptionField, self).__init__(*args, **kwargs)