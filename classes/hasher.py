import hashlib, base64
from django.conf import settings
from base_crypter import BaseCrypter


class Hasher(BaseCrypter):
    
    def __init__(self, *args, **kwargs):
        self.encrypted_salt = settings.SALT
        self.length = 64
        self.iterations = 10
        
    def create_new_salt(self, value):
        return base64.b64encode(self.rsa_encrypt(value))
         
    def get_salt(self):
        return self.rsa_decrypt(self.encrypted_salt)

    def get_hash(self, value, salt=None):
        """ for a given value, return a salted SHA256 hash """
        
        if not value:
            retval = None
        else:
            # only change algorithm if existing hashes have been updated
            if not salt:
                salt = self.get_salt()
            if not isinstance(salt, str):
                raise TypeError('Hasher expects \'salt\' to be a string.')
            hlib = hashlib.sha256()
            hlib.update(salt)
            hlib.update(value)
            hash_value = hlib.hexdigest()
            retval = hash_value
            #if len(hash_value) != self.length:
            #    raise TypeError('Invalid hash_text length, expected %s. Got %s' % (self.length, len(hash_value)))
        return retval