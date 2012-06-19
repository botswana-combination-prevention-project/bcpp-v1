import base64, os
from datetime import datetime
from M2Crypto import Rand, RSA, Cipher
from bhp_crypto.models import Crypt
from hasher import Hasher

# http://chandlerproject.org/Projects/MeTooCrypto
# http://www.topdog.za.net/2012/03/27/generating-cryptography-keys-in-python/
# http://en.wikipedia.org/wiki/RSA_%28algorithm%29
# http://en.wikipedia.org/wiki/Optimal_Asymmetric_Encryption_Padding
            
        
class Crypter(object):
    
    """
    Uses M2Crypto.RSA public key encryption
    crypter = Crypter()
    self.crypter.public_key = settings.PUBLIC_KEY_STRONG
    self.crypter.private_key = settings.PRIVATE_KEY_STRONG
    
    #encrypt
    value = self.crypter.encrypt(value)
    
    #decrypt
    value = self.crypter.decrypt(value)
    """
    # prefix for each segment of an encrypted value, also used to calculate field length for model.
    prefix = 'enc1:::' # uses a prefix to flag as encrypted like django_extensions does
    cipher_prefix = 'enc2:::'
    KEY_LENGTH = 4096
    ALGORITHM = None # ('RSA', 'AES')
    ENC=1
    DEC=0
    # hasher
    hasher = Hasher()
    
    def __init__(self, *args, **kwargs):
        self.public_key = None
        self.private_key = None
        

    def set_public_key(self, keyfile):
        """ load public key """
        if keyfile:
            self.public_key = RSA.load_pub_key(keyfile)
        
    def set_private_key(self, keyfile):
        """ load the private key """
        if keyfile:
            self.private_key = RSA.load_key(keyfile)

    def set_key(self, key="123452345"):
        """ load the key """
        self.key = base64.b64encode(key)
    
    def build_cipher(self, key, iv=None, op=ENC):
        """"""""
        return Cipher(alg='aes_128_cbc', key=key, iv=iv, op=op)
    
    def _blank_callback(self): 
        "Replace the default dashes as output upon key generation" 
        return
    
    def create_new_key_pair(self):
        """ create a new key-pair in the default folder, filename includes the current timestamp """        
        # have a suffix to the file names to prevent overwriting
        name = str(datetime.today())
        # Random seed 
        Rand.rand_seed (os.urandom (self.KEY_LENGTH)) 
        # Generate key pair 
        key = RSA.gen_key (self.KEY_LENGTH, 65537, self._blank_callback) 
        # Non encrypted key 
        key.save_key('user-private.pem.%s' % name, None) 
        # Use a pass phrase to encrypt key 
        #key.save_key('user-private.pem') 
        key.save_pub_key('user-public.pem.%s' % name)         
    
    def encrypt(self, value, update_lookup=False):
        """ return the encrypted field value (hash+cipher), do not override """
        def aes_encrypt(value):            
            cipher = self.build_cipher(self.key)
            v = cipher.update(value)
            v = v + cipher.final()
            del cipher
            return v
        
        def rsa_encrypt(value):
            return self.public_key.public_encrypt(value, RSA.pkcs1_oaep_padding)
        
        if not value:
            encrypted_value = value    
        else:    
            if not self.is_encrypted(value):
                if self.ALGORITHM == 'AES':
                    cipher_text = aes_encrypt(value)
                elif self.ALGORITHM == 'RSA':
                    if len(value) >= self.KEY_LENGTH/24:
                        raise ValueError('String value to encrypt may not exceed {0} characters. Got {1}.'.format(self.KEY_LENGTH/24,len(value)))
                    cipher_text = rsa_encrypt(value)
                else:
                    raise ValueError('Cannot determine algorithm for encryption')
                hash_text = self.get_hash(value)
                encoded_cipher_text = base64.b64encode(cipher_text)
                encrypted_value = self.prefix + hash_text + self.cipher_prefix + encoded_cipher_text
                if update_lookup:
                    # normally this is done via the pre_save signal
                    self.update_cipher_lookup(encrypted_value)
            else:
                encrypted_value = value    
        return encrypted_value        

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
                    # this is an error condition
                    raise TypeError('Expected cipher text for given new hash, but got None.')
            
    def get_hash(self, value):
        """ hash is stored for exact match search functionality as the cipher is never the same twice """
        if self.is_encrypted(value):
            # if value is an encrypted value string, cut out the hash segment
            hash_text = value[len(self.prefix):][:self.hasher.length]
            #hash_text = value[len(self.prefix):].split(self.cipher_prefix)[0]
        else:
            # if the value is not encrypted, hash it.
            hash_text = self.hasher.get_hash(value)
        ret_val = hash_text
        return ret_val        

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
    
    def decrypt(self, value):
        """ if private key is known, return an decrypted value, otherwise return the encrypted value """
        if value:
            if self.private_key:
                if self.is_encrypted(value):
                    hash_text = self.get_hash(value)
                    cipher_text = self.get_cipher(value, hash_text)
                    if cipher_text:
                        value = self.private_key.private_decrypt(base64.b64decode(cipher_text),
                                                                 RSA.pkcs1_oaep_padding).replace('\x00', '')
                    else:
                        raise ValueError('When decrypting, expected to find cipher for given hash %s' % (hash_text,))
            else:
                # if there is no private key, we must always return an encrypted value, unless None!
                if not self.is_encrypted(value):
                    # for some reason, the value was not encrypted AND we do not
                    # have a private key, so it should be 
                    value = self.encrypt(value)
        return value  
        