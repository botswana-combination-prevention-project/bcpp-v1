import hashlib, base64, os
from datetime import datetime
from django.core.exceptions import ValidationError
from base_crypter import BaseCrypter


class Hasher(BaseCrypter):
    """ handle all hashing """
    def __init__(self, *args, **kwargs):
        self.length = self._get_hash_length()
        self.iterations = 40
        super(Hasher, self).__init__(*args, **kwargs)

    def new_hasher(self, value=''):
        return hashlib.sha256(value)
         
    def create_new_salt(self, length=12, allowed_chars='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#%^&*()?<>.,[]{}', suffix=str(datetime.today())):
        if not self.public_key:
            self.set_public_key(self.valid_modes.get('rsa').get('local-rsa').get('public'))
        salt = self.rsa_encrypt(self.make_random_salt(length, allowed_chars), algorithm='rsa', mode='local-rsa')
        path = '{0}{1}'.format(self.valid_modes.get('salt'), suffix)
        f = open(path, 'w') 
        f.write(base64.b64encode(salt))
        f.close()
        return base64.b64encode(salt)
    
    def get_salt(self):
        if not self.encrypted_salt:
            self._get_encrypted_salt()
        return self.rsa_decrypt(self.encrypted_salt, algorithm='rsa', mode='local-rsa')
    
    def _get_hash_length(self):
        return hashlib.sha256('Foo').block_size
        
    def get_hash(self, value):
        """ for a given value, return a salted SHA256 hash """
        if not value:
            retval = None
        else:
            salt = self.get_salt()
            if not isinstance(salt, str):
                raise ValidationError('The Encryption keys are not available to this system. Unable to save sensitive data.')
            digest = self.new_hasher(salt+value).digest()
            # iterate
            for x in range(0, self.iterations-1):
                digest = self.new_hasher(digest).digest()
            hash_value = digest.encode("hex")
            retval = hash_value
        return retval
    
    
    
