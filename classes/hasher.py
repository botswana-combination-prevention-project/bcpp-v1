import hashlib, base64
from datetime import datetime
from django.core.exceptions import ValidationError
from base_crypter import BaseCrypter


class Hasher(BaseCrypter):
    """ handle all hashing """
    def __init__(self, *args, **kwargs):
        self.encrypted_salt=self.read_salt_from_file()
        self.length=self._get_hash_length()
        self.iterations=40
        super(Hasher, self).__init__( *args, **kwargs)
        #orivate key needed to get the salt
        self.set_private_key(self.get_local_rsa_private_keyfile())

    def new_hasher(self, value=''):
        return hashlib.sha256(value)
         
    def create_new_salt(self, length=12, allowed_chars='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#%^&*()?<>.,[]{}', suffix=str(datetime.today())):
        salt=self.rsa_encrypt(self.make_random_salt(), algorithm='rsa', mode='local-rsa')
        path='{0}{1}'.format(self.valid_modes.get('salt'), suffix)
        f=open(path, 'w') 
        f.write(base64.b64encode(salt))
        f.close()
        return base64.b64encode(salt)
    
    def read_salt_from_file(self):
        path=self.valid_modes.get('salt')
        try:
            f=open(path,'r')
            retval=f.read()
        except:
            print 'Unable to open {0}'.format(path)
            retval=None
        return retval    
    
    def get_salt(self):
        if self.private_key:
            return self.rsa_decrypt(self.encrypted_salt)
    
    def _get_hash_length(self):
        return hashlib.sha256('Foo').block_size
        
    def get_hash(self, value):
        """ for a given value, return a salted SHA256 hash """
        if not value:
            retval=None
        else:
            # only change algorithm if existing hashes have been updated
            salt=self.get_salt()
            if not isinstance(salt, str):
                raise ValidationError('The Encryption keys are not available to this system. Unable to save sensitive data.')
            digest=self.new_hasher(salt+value).digest()
            # then hash 40-1 times
            for x in range(0, self.iterations-1):
                digest=self.new_hasher(digest).digest()
            hash_value=digest.encode("hex")
            retval=hash_value
        return retval
    
    
    