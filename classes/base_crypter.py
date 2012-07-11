import os, base64
from datetime import datetime
from M2Crypto import Rand, RSA, EVP
from django.core.exceptions import ImproperlyConfigured
from base import Base
from bhp_crypto.settings import settings


class BaseCrypter(Base):
    
    KEY_LENGTH = 2048
    ENC=1
    DEC=0
    #used to refer to files dictionary
    valid_rsa_key_types=['irreversible','restricted', 'local']
    #default filenames for the pem files, salt and aes key
    #the "keys" in this dictionary may NOT be changed
    files={
        'irreversible-public': 'user-public-irreversible.pem',
        'restricted-public': 'user-public-restricted.pem',
        'restricted-private': 'user-private-restricted.pem',
        'local-public': 'user-public-local.pem',
        'local-private': 'user-private-local.pem',
        'local-aes': 'user-aes-local.pem',
        'salt': 'user-encrypted-salt.pem'}
 
    
    def __init__(self, *args, **kwargs):
        self.public_key=None
        self.private_key=None
        self.aes_key=None
        self.algorithm=None
        self.mode=None
        
    def set_public_key(self, keyfile):
        """ load public key using the pem filename """
        if keyfile:
            self.public_key = RSA.load_pub_key(keyfile)
        
    def set_private_key(self, keyfile):
        """ load the private key using the pem filename """
        
        if keyfile:               
            try:
                self.private_key = RSA.load_key(keyfile)
            except:
                print 'Failed to load private key {0}.'.format(keyfile)
                                
    def set_aes_key(self, keyfile="user-aes-local.pem"):
        """ Decrypt and set the AES key from a file using the local private key.
        Private key must be set before calling """
        self.aes_key = ''
        if keyfile:
            f = open(keyfile, 'r')
            encrypted_key = f.read()
            f.close()
            if self.private_key:
                self.aes_key = self.rsa_decrypt(encrypted_key)
    
    def get_private_key_local_keyfile(self):
        self.private_keyfile = None
        if not hasattr(settings, 'PRIVATE_KEY_LOCAL'):
            raise ImproperlyConfigured('For \'%s\' security, you must set the PRIVATE_KEY_LOCAL setting to ' \
                                        'point to your public key (path and filename).' % (self.mode,))
        return settings.PRIVATE_KEY_LOCAL
    
    def get_aes_key(self):
        """ """
        retval = None
        if 'AES_KEY' in dir(settings):
            if settings.AES_KEY:
                retval = settings.AES_KEY
        return retval  
       
    def _blank_callback(self): 
        "Replace the default dashes as output upon key generation" 
        return
    
    def create_new_rsa_key_pairs(self, suffix=str(datetime.today())):
        """ Create a new key-pair in the default folder, filename includes the current timestamp to avoid overwriting as existing key.
        * For now this can be called in the shell. 
        * Filename includes the current timestamp to avoid overwriting as existing key """        
        for key_type in self.valid_rsa_key_types:
            print key_type
            # Random seed 
            Rand.rand_seed (os.urandom (self.KEY_LENGTH)) 
            # Generate key pair 
            key = RSA.gen_key (self.KEY_LENGTH, 65537, self._blank_callback) 
            # create and save the public key to file
            filename=[filename for k,filename in self.files.iteritems() if key_type+'-public' in k] 
            # key.save_pub_key('user-private-local.pem'), for example if suffix=''            
            key.save_pub_key(''.join(filename)+suffix) 
            # create and save the private key to file
            filename=[filename for k,filename in self.files.iteritems() if key_type+'-private' in k] 
            # key.save_key('user-private-local.pem'), for example if suffix=''
            if filename:
                key.save_key(''.join(filename)+suffix, None) 
       
    
    def create_aes_key(self, public_keyfile=files.get('local-public'), suffix=str(datetime.today()), key=None):
        """ create and encrypt a new AES key. Use the "local" public key.
        * Filename suffix is added to the filename to avoid overwriting an existing key """        
        if not key:
            key = self.get_random_string()
        if not public_keyfile:
            raise TypeError('Please specify the local public key filename. Got None')
        self.set_public_key(public_keyfile)
        filename=[filename for k,filename in self.files.iteritems() if 'local-aes' in k]
        filename=''.join(filename)+suffix
        encrypted_aes_key = self.public_key.public_encrypt(key, RSA.pkcs1_oaep_padding)   
        f = open(filename, 'w') 
        f.write(base64.b64encode(encrypted_aes_key))
        f.close()
        #return base64.b64encode(encrypted_aes_key)
    
    def rsa_encrypt(self, value):
        """Return an uncode encrypted value, but know that it may fail if keys are not available"""
        if not self.public_key:
            raise ImproperlyConfigured("RSA public key not set, unable to decrypt cipher.")
        return self.public_key.public_encrypt(value, RSA.pkcs1_oaep_padding)
    
    def rsa_decrypt(self, cipher_text, is_encoded=True):
        """ Return cleaned decrypted cipher text if the private key is available. 
        Check for the private_key before calling this method.
        Cipher_text is base64 encoded unless is_encoded is false"""
        
        if not self.private_key:
            raise ImproperlyConfigured("RSA private key not set, unable to decrypt cipher.")
        if is_encoded:
            cipher_text = base64.b64decode(cipher_text)
        return self.private_key.private_decrypt(cipher_text,
                                                RSA.pkcs1_oaep_padding).replace('\x00', '')
    
    def _build_cipher(self, key, iv=None, op=ENC):
        """"""""
        if iv is None:
                iv = '\0' * 16
        else:
            iv = base64.b64decode(iv)
        return EVP.Cipher(alg='aes_128_cbc', key=key, iv=iv, op=op)
                                                    
    def aes_decrypt(self, cipher_text, is_encoded=True):
        """ Decrypt a AES cipher using a secret key that itself is decrypted using the private key. """
        retval = cipher_text
        if not self.aes_key:
            raise ImproperlyConfigured("AES key not set, unable to decrypt cipher.")
        else:    
            if is_encoded:
                cipher_text = base64.b64decode(cipher_text)
            cipher = self._build_cipher(self.aes_key, None, self.DEC)
            v = cipher.update(cipher_text)
            v = v + cipher.final()
            del cipher
            retval = v.replace('\x00', '')
        return retval
    
    def aes_encrypt(self, value):            
        """ Encrypt with AES, but fail if aes_key unavailable.
        Important to not allow any data to be saved if the keys are not available"""
        
        if not self.aes_key:
            raise ImproperlyConfigured('AES key not available, unable to encrypt sensitive data using the AES algorithm.')
        else:    
            cipher = self._build_cipher(self.aes_key, None, self.ENC)
            v = cipher.update(value)
            v = v + cipher.final()
            del cipher
        return v


    
