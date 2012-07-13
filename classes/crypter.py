import base64
#from django.core.exceptions import ImproperlyConfigured
from base_crypter import BaseCrypter
from bhp_crypto.models import Crypt
from hasher import Hasher

# http://chandlerproject.org/Projects/MeTooCrypto
# http://www.topdog.za.net/2012/03/27/generating-cryptography-keys-in-python/
# http://en.wikipedia.org/wiki/RSA_%28algorithm%29
# http://en.wikipedia.org/wiki/Optimal_Asymmetric_Encryption_Padding   
        
        
class Crypter(BaseCrypter):

    hasher = Hasher()
    
    def __init__(self, *args, **kwargs):
        super(Crypter, self).__init__(self, *args, **kwargs)
        
    def encrypt(self, value, **kwargs):
        """ return the encrypted field value (hash+cipher) where secret is secret or secret_iv, do not override """       
        update_lookup=kwargs.get('update_lookup', False)
        if not value:
            hash_secret=value    
        else:    
            if not self.is_encrypted(value):
                if self.algorithm=='aes':
                    encoded_secret=self.iv_prefix.join(map(base64.b64encode, self.aes_encrypt(value)))
                elif self.algorithm=='rsa':
                    if len(value)>=self.KEY_LENGTH/24:
                        raise ValueError('String value to encrypt may not exceed {0} characters. Got {1}.'.format(self.KEY_LENGTH/24,len(value)))
                    encoded_secret=base64.b64encode(self.rsa_encrypt(value))
                else:
                    raise ValueError('Cannot determine algorithm to use for encryption. Valid options are {0}. Got {1}'.format(', '.join(self.valid_modes.keys()), self.algorithm))
                hash_text=self.get_hash(value)
                hash_secret=self.hash_prefix+hash_text+self.secret_prefix+encoded_secret
                if update_lookup:
                    # normally this is done via the pre_save signal??
                    self.update_secret_in_lookup(hash_secret)
            else:
                hash_secret=value    
        return hash_secret        
    
    def decrypt(self, secret, secret_is_hash=True, **kwargs):
        """ Decrypt secret and if secret is a hash, use hash to lookup the real secret first.
        
        Do not assume secret is an encrypted value, look for hash_prefix or secret prefix.
        By default we expect secret to be the stored field value -- which is a hash.
        If we decide to use this method where the secret is not a hash, then the prefix is 
        the secret_prefix and the lookup is skipped."""
        plaintext=secret
        if secret:
            prefix=lambda x:self.hash_prefix if x else self.secret_prefix
            if self.is_encrypted(secret, prefix(secret_is_hash)):
                if secret_is_hash:
                    hash_text=self.get_hash(secret)
                    secret=self.get_secret_from_string(secret, hash_text)
                else:
                    secret=secret[len(self.secret_prefix):]
                if secret:
                    if self.algorithm=='aes':
                        if self.set_aes_key():
                            plaintext=self.aes_decrypt(secret.partition(self.iv_prefix))
                    elif self.algorithm=='rsa':
                        if self.set_private_key():
                            plaintext=self.rsa_decrypt(secret)
                    else:
                        raise ValueError('Cannot determine algorithm for decryption. Valid options are {0}. Got {1}'.format(', '.join(self.valid_modes.keys()), self.algorithm))
                else:
                    raise ValueError('When decrypting, expected to find cipher for given hash {0}'.format(hash_text))
        return plaintext
    
    def update_secret_in_lookup(self, hash_secret):
        """ update a model to have a reference of hash_value / cipher_value pairs """
        if hash_secret:
            # get and update or create the crypt model with this hash, cipher pair
            hash_text=self.get_hash(hash_secret)
            secret=self.get_secret_from_hash_secret(hash_secret, hash_text)
            if Crypt.objects.filter(hash=hash_text):
                if secret:
                    crypt=Crypt.objects.get(hash=hash_text)
                    crypt.secret=secret
                    crypt.save()
            else:
                if secret:
                    Crypt.objects.create(hash = hash_text, 
                                         secret = secret,
                                         algorithm = self.algorithm,
                                         mode = self.mode)
                else:
                    # if the hash is not in the crypt model and you do not have a cipher
                    # update: if performing a search, instead of data entry, the hash may not exist
                    print 'hash not found in crypt model. {0} {1} {2}'.format(self.algorithm, self.mode, hash_text)
                    #raise TypeError('Expected cipher text for given {0} {1} hash, but got None for value {2}, {3}.'.format(self.algorithm, self.mode, secret, hash_text))
            
    def get_hash(self, value):
        """ hash is stored for exact match search functionality as the cipher is never the same twice """
        if self.is_encrypted(value):
            # if value is an encrypted value string, cut out the hash segment
            hash_text=value[len(self.hash_prefix):][:self.hasher.length]
            #hash_text = value[len(self.hash_prefix):].split(self.secret_prefix)[0]
        else:
            # if the value is not encrypted, hash it.
            # note that hash must be unique for each mode and algorithm
            #if not self.:
            #    raise TypeError('Subclass must set the mode and algorithm to make a salt to ensure a unique hash.')
            hash_text=self.hasher.get_hash(value)
        ret_val=hash_text
        return ret_val        
    
    def get_stored_hash(self, value):
        return self.hash_prefix+self.get_hash(value)
    
    def get_secret_from_hash_secret(self, hash_secret, hash_text):
        """ Return the secret from within the hash_secret or from a lookup if hash_secret is just the hash"""
        if not hash_secret:
            retval=None
        else:
            if self.is_encrypted(hash_secret):
                # split on hash, but if this is a hash only, secret_string will be None
                secret=hash_secret[len(self.hash_prefix)+len(hash_text)+len(self.secret_prefix):]
                if not secret:
                    # lookup secret_string for this hash_text
                    secret=self._lookup_secret(hash_text)
                retval=secret    
            else:
                raise ValueError('Value must be encrypted or None.')
            return retval

    def _lookup_secret(self, hash_text):
        """ Given a hash, lookup cipher in Crypt model. 
        Will be called by get_secret_from_string if secret is not in the 'encrypted value' (e.g. is a hash) """
        if Crypt.objects.filter(hash=hash_text):
            crypt=Crypt.objects.get(hash=hash_text)
            ret_val=crypt.secret
        else:
            ret_val=None    
        return ret_val
    
      
        