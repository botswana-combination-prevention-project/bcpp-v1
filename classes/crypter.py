import base64
from django.core.exceptions import ImproperlyConfigured
from base_crypter import BaseCrypter
from bhp_crypto.models import Crypt
from hasher import Hasher

# http://chandlerproject.org/Projects/MeTooCrypto
# http://www.topdog.za.net/2012/03/27/generating-cryptography-keys-in-python/
# http://en.wikipedia.org/wiki/RSA_%28algorithm%29
# http://en.wikipedia.org/wiki/Optimal_Asymmetric_Encryption_Padding   
        
        
class Crypter(BaseCrypter):
    
    """   """
    # prefix for each segment of an encrypted value, also used to calculate field length for model.
    prefix = 'enc1:::' # uses a prefix to flag as encrypted like django_extensions does
    cipher_prefix = 'enc2:::'

    # hasher
    hasher = Hasher()
    
    def __init__(self, *args, **kwargs):
        super(Crypter, self).__init__(self, *args, **kwargs)
    
    @property
    def extra_salt(self):
        """salt for hashes"""
        if self.algorithm not in self.valid_modes.keys():
            raise ImproperlyConfigured('Invalid encryption algorithm. Got {0}. Valid options are {1}'.format(self.algorithm, ', '.join(self.valid_modes.keys())))
        if self.mode not in self.valid_modes.get(self.algorithm).keys():
            raise ImproperlyConfigured('Invalid encryption mode. Got {0}. Valid options are {1}'.format(self.mode, ', '.join(self.valid_modes.get(self.algorithm).keys())))
        return self.algorithm+self.mode.replace(' ', '')
    
    def encrypt(self, value, **kwargs):
        """ return the encrypted field value (hash+cipher), do not override """
        if not self.extra_salt:
            raise ImproperlyConfigured('Instance attribute \'extra_salt\' is required. Got None')
        update_lookup=kwargs.get('update_lookup', False)
        if not value:
            encrypted_value = value    
        else:    
            if not self.is_encrypted(value):
                if self.algorithm == 'aes':
                    cipher_text = self.aes_encrypt(value)
                elif self.algorithm == 'rsa':
                    if len(value) >= self.KEY_LENGTH/24:
                        raise ValueError('String value to encrypt may not exceed {0} characters. Got {1}.'.format(self.KEY_LENGTH/24,len(value)))
                    cipher_text = self.rsa_encrypt(value)
                else:
                    raise ValueError('Cannot determine algorithm to use for encryption. Valid options are {0}. Got {1}'.format(', '.join(self.valid_modes.keys()), self.algorithm))
                hash_text = self.get_hash(value)
                encoded_cipher_text = base64.b64encode(cipher_text)
                encrypted_value = self.prefix + hash_text + self.cipher_prefix + encoded_cipher_text
                if update_lookup:
                    # normally this is done via the pre_save signal
                    self.update_cipher_lookup(encrypted_value)
            else:
                encrypted_value = value    
        return encrypted_value        
    
    def decrypt(self, value, **kwargs):
        """ if private key is known, return an decrypted value, otherwise return the encrypted value """
        if not self.extra_salt:
            raise ImproperlyConfigured('Instance attribute \'extra_salt\' is required. Got None')
        if value:
            if self.private_key:
                if self.is_encrypted(value):
                    hash_text = self.get_hash(value)
                    cipher_text = self.get_cipher(value, hash_text)
                    if cipher_text:
                        if self.algorithm == 'aes':
                            value = self.aes_decrypt(cipher_text)
                        elif self.algorithm == 'rsa':
                            value = self.rsa_decrypt(cipher_text)
                        else:
                            raise ValueError('Cannot determine algorithm for decryption. Valid options are {0}. Got {1}'.format(', '.join(self.valid_modes.keys()), self.algorithm))
                    else:
                        raise ValueError('When decrypting, expected to find cipher for given hash {0}'.format(hash_text))
        #            else:
        #                # if there is no private key, we must always return an encrypted value, unless None!
        #                if not self.is_encrypted(value):
        #                    # for some reason, the value was not encrypted AND we do not
        #                    # have a private key, so it should be 
        #                    value = self.encrypt(value, **kwargs)
        return value
    
    def update_cipher_lookup(self, encrypted_value):
        """ update a model to have a reference of hash_value / cipher_value pairs """
        if encrypted_value:
            # get and update or create the crypt model with this hash, cipher pair
            hash_text = self.get_hash(encrypted_value)
            cipher_text = self.get_cipher(encrypted_value, hash_text)
            if Crypt.objects.filter(hash_text=hash_text):
                if cipher_text:
                    crypt = Crypt.objects.get(hash_text=hash_text)
                    crypt.cipher_text = cipher_text
                    crypt.save()
            else:
                if cipher_text:
                    Crypt.objects.create(hash_text=hash_text, cipher_text=cipher_text)
                else:
                    # if the hash is not in the crypt model and you do not have a cipher
                    # update: if performing a search, instead of data entry, the hash may not exist
                    print 'hash not found in crypt model. {0} {1} {2}'.format(self.algorithm, self.mode, hash_text)
                    #raise TypeError('Expected cipher text for given {0} {1} hash, but got None for value {2}, {3}.'.format(self.algorithm, self.mode, encrypted_value, hash_text))
            
    def get_hash(self, value):
        """ hash is stored for exact match search functionality as the cipher is never the same twice """
        if self.is_encrypted(value):
            # if value is an encrypted value string, cut out the hash segment
            hash_text = value[len(self.prefix):][:self.hasher.length]
            #hash_text = value[len(self.prefix):].split(self.cipher_prefix)[0]
        else:
            # if the value is not encrypted, hash it.
            # note that hash must be unique for each mode and algorithm
            if not self.extra_salt:
                raise TypeError('Subclass must set the mode and algorithm to make a salt to ensure a unique hash.')
            hash_text = self.hasher.get_hash(value, self.extra_salt)
        ret_val = hash_text
        return ret_val        
    
    def get_stored_hash(self, value):
        return self.prefix+self.get_hash(value)
    
    def get_cipher(self, encrypted_value, hash_text):
        """ Return the cipher string from within the encrypted value or from a lookup """
        if not encrypted_value:
            retval = None
        else:
            if self.is_encrypted(encrypted_value):
                # split on hash, but if this is a hash only, cipher_text will be None
                cipher_text = encrypted_value[len(self.prefix)+len(hash_text)+len(self.cipher_prefix):]
                if not cipher_text:
                    # lookup cipher_text for this hash_text
                    cipher_text = self._get_cipher_lookup(hash_text)
                retval = cipher_text    
            else:
                raise ValueError('Value must be encrypted or None.')
            return retval

    def _get_cipher_lookup(self, hash_text):
        """ Given a hash, lookup cipher in Crypt model. 
        
        Will be called by get_cipher if cipher is not in the 'encrypted value' (e.g. is a hash) 
        """
        if Crypt.objects.filter(hash_text=hash_text):
            crypt = Crypt.objects.get(hash_text=hash_text)
            ret_val = crypt.cipher_text
        else:
            ret_val = None    
        return ret_val
    
    def is_encrypted(self, value):
        """ The value string is considered encrypted if it starts with 'self.prefix' """
        if not value:
            retval = False
        else:
            if value == self.prefix:
                raise TypeError('Expected a string value, got just the encryption prefix.')
            if value.startswith(self.prefix):
                retval = True
            else:
                retval = False
        return retval
    
    def mask_encrypted(self, value, mask='<encrypted>'):
        """ help format values for display by masking them if encrypted at the time of display"""
        if self.is_encrypted(value):
            return mask
        else:
            return value
    
      
        