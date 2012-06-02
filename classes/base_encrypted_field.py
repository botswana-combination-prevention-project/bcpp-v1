import base64
from M2Crypto import RSA
from django.db import models
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from hasher import Hasher



class BaseEncryptedField(models.Field):
    
    """ store both a SHA-256 hash-value for exact comparison when searching and a cipher generated 
    using a public key which can be decrypted if the private key is available on the system. Hash 
    and cipher are stored as one string prefixed by the 'prefix' and can be split on 
    the 'cipher_prefix' """

    prefix = 'enc1:::' # uses a prefix to flag as encrypted like django_extensions does
    cipher_prefix = 'enc2:::'

    def to_python(self, value):
        """ return the decrypted value if a private key is found, otherwise remains encrypted. """
        if value:
            retval = self.decrypt(value)
        else:
            retval = value
        return retval
    
    def get_prep_value(self, value):
        if value:
            value = self.encrypt(value)   
        return super(BaseEncryptedField, self).get_prep_value(value)

    def encrypt(self, value):
        """ return the encrypted field value (hash+cipher), do not override """
        # http://en.wikipedia.org/wiki/RSA_%28algorithm%29
        # http://en.wikipedia.org/wiki/Optimal_Asymmetric_Encryption_Padding
        
        if not settings.PUBLICKEY:
            raise ImproperlyConfigured('Improperly Configured. Settings attribute PUBLICKEY is required for encrypted fields.')
        if not self.is_encrypted(value):
            writer = RSA.load_pub_key(settings.PUBLICKEY)
            cipher = writer.public_encrypt(value, RSA.pkcs1_oaep_padding)
            hash_value = self.get_hash(value)
            value = self.prefix + hash_value + self.cipher_prefix + base64.b64encode(cipher)
        return value        

    def get_hash(self, value):
        """ hash is stored for exact match search functionality as the cipher is never the same twice """
        if value.startswith(self.prefix):
            ret_val = value[len(self.prefix):].split(self.cipher_prefix)[0]
        else:
            hasher = Hasher()
            hash_value = hasher.get_hash(value).hexdigest()
            # return the hash_value base64 encoded
            # ret_val = base64.b64encode(hash_value)
            ret_val = hash_value
        return ret_val        

    def is_encrypted(self, value):
        """ this is a encrypted if it has my prefix"""
        if value.startswith(self.prefix):
            retval = True
        else:
            retval = False
        return retval

    def decrypt(self, value):
        """ if private key is available, then return a decrypted value, otherwise return an encrypted value """

        if 'PRIVATEKEY' in dir(settings):
            if settings.PRIVATEKEY:
                if self.is_encrypted(value):
                    private_key = RSA.load_key (settings.PRIVATEKEY)
                    cipher = value[len(self.prefix):].split(self.cipher_prefix)[1]
                    value = private_key.private_decrypt(base64.b64decode(cipher), RSA.pkcs1_oaep_padding).replace('\x00','')
        else:
            if not self.is_encrypted(value):
                value = self.encrypt(value)
        return value

