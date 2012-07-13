import os, base64
from datetime import datetime
from M2Crypto import Rand, RSA, EVP
from django.core.exceptions import ImproperlyConfigured
from django.conf import settings
from base import Base


class BaseCrypter(Base):
    
    KEY_LENGTH=2048
    ENC=1
    DEC=0
    # prefix for each segment of an encrypted value, also used to calculate field length for model.
    hash_prefix='enc1:::' # uses a prefix to flag as encrypted like django_extensions does
    secret_prefix='enc2:::'
    iv_prefix='iv:::'
    #default filenames for the pem files, salt and aes key
    #the "keys" in this dictionary may NOT be changed
    try:
        key_path=settings.KEY_PATH
    except KeyError:
        key_path=''    
    valid_modes={
        'rsa': {'irreversible-rsa': {'public': os.path.join(key_path,'user-public-irreversible.pem')},
                'restricted-rsa': {'public': os.path.join(key_path,'user-public-restricted.pem'),'private': os.path.join(key_path,'user-private-restricted.pem')},
                'local-rsa':{'public': os.path.join(key_path,'user-public-local.pem'),'private': os.path.join(key_path,'user-private-local.pem')},
                },
        'aes': {'local-aes': os.path.join(key_path,'user-aes-local')},
        'salt': os.path.join(key_path,'user-encrypted-salt')
            }
 
    def __init__(self, *args, **kwargs):
        
        self.public_key=None
        self.private_key=None
        self.aes_key=None
        self.algorithm=None
        self.mode=None
        
    def set_public_key(self, keyfile=None, **kwargs):
        """ load public key using the pem filename. """
        if not self.public_key:
            algorithm=kwargs.get('algorithm', self.algorithm)
            mode=kwargs.get('mode', self.mode)
            if not keyfile:
                # keyfile not specified, so get the default for this algorithm and mode
                if not algorithm or not mode:
                    raise AttributeError('Algorithm and mode must be set before attempting to set the public key')
                keyfile=self.valid_modes.get(algorithm).get(mode).get('public')
            try:
                self.public_key=RSA.load_pub_key(keyfile)
            except:
                print 'warning: failed to load public key {0}.'.format(keyfile)
        return self.public_key!=None

    def set_private_key(self, keyfile=None, **kwargs):
        """ load the private key using the pem filename """
        if not self.private_key:
            algorithm=kwargs.get('algorithm', self.algorithm)
            mode=kwargs.get('mode', self.mode)
            if not keyfile:
                # keyfile not specified, so get the default for this algorithm and mode
                if not algorithm or not mode:
                    raise AttributeError('Algorithm and mode must be set before attempting to set the private key')
                keyfile=self.valid_modes.get(algorithm).get(mode).get('private')
            try:
                self.private_key=RSA.load_key(keyfile)
            except:
                # if you need a warning here, do so in the subclass
                pass
        return self.private_key!=None
    
    def set_aes_key(self):
        """ Decrypt and set the AES key from a file using the local-rsa private key. """
        if not self.aes_key:
            try:
                f = open(self.get_aes_keyfile(), 'r')
                secret_key = f.read() 
                f.close()
                self.aes_key = self.rsa_decrypt(secret_key, algorithm='rsa', mode='local-rsa')
            except:
                print 'warning: failed to load aes key {0}.'.format(self.get_aes_keyfile())
        return self.aes_key!=None
            
    def get_local_rsa_private_keyfile(self):
        return self.valid_modes.get('rsa').get('local-rsa').get('private')
    
    def get_aes_keyfile(self):            
        return self.valid_modes.get('aes').get('local-aes')
    
    def create_new_rsa_key_pairs(self, suffix=str(datetime.today())):
        """ Create a new key-pair in the default folder, filename includes the current timestamp to avoid overwriting as existing key.
        * For now this can be called in the shell. 
        * Filename includes the current timestamp to avoid overwriting as existing key """        
        def _blank_callback(self): 
            "Replace the default dashes as output upon key generation" 
            return
        
        for mode_pair in self.valid_modes.get('rsa').itervalues():
            # Random seed 
            Rand.rand_seed (os.urandom (self.KEY_LENGTH)) 
            # Generate key pair 
            key = RSA.gen_key (self.KEY_LENGTH, 65537, _blank_callback) 
            # create and save the public key to file
            filename=mode_pair.get('public', None)
            # key.save_pub_key('user-private-local.pem'), for example if suffix=''            
            key.save_pub_key(''.join(filename)+suffix) 
            # create and save the private key to file
            filename=mode_pair.get('private', None)
            # key.save_key('user-private-local.pem'), for example if suffix=''
            if filename:
                key.save_key(''.join(filename)+suffix, None) 
    
    def create_aes_key(self, suffix=str(datetime.today()), key=None):
        """ create and rsa encrypt a new AES key. Use the "local" public key.
        * Filename suffix is added to the filename to avoid overwriting an existing key """        
        if not key:
            key=os.urandom(16)
        filename=self.valid_modes.get('aes').get('local-aes')+suffix
        secret_aes_key=self.rsa_encrypt(key, algorithm='rsa', mode='local-rsa')   
        f=open(filename, 'w') 
        f.write(base64.b64encode(secret_aes_key))
        f.close()
    
    def rsa_encrypt(self, plaintext, **kwargs):
        """Return an unencode secret, but know that it may fail if keys are not available"""
        if not self.set_private_key(**kwargs):
            # must FAIL here if key not available and user is trying to save data
            raise ImproperlyConfigured('RSA key not available, unable to encrypt sensitive data using the RSA algorithm.')        
        if self.is_encrypted(plaintext):
            raise ValueError('Attempt to rsa encrypt an already encrypted value.')
        return self.public_key.public_encrypt(plaintext, RSA.pkcs1_oaep_padding)
    
    def rsa_decrypt(self, secret, is_encoded=True, **kwargs):
        """ Return cleaned decrypted secret if the private key is available. 
        Check for the private_key before calling this method.
        Secret is base64 encoded unless 'is_encoded' is false"""
        retval=secret
        if self.set_private_key(**kwargs):
            if is_encoded:
                secret = base64.b64decode(secret)
            retval=self.private_key.private_decrypt(secret,RSA.pkcs1_oaep_padding).replace('\x00', '')
        return retval
                                                    
    def aes_decrypt(self, secret, is_encoded=True):
        """ Used a random iv stored with the secret, so takes a tuple (secret_text, sep, iv).
        Will return either the plaintext or the tuple  """
        retval=secret
        if isinstance(secret, (list, tuple)):
            #cipher_tuple is (cipher, sep, iv)
            secret_text,iv=secret[0], secret[2]
        else:
            print 'warning: aes cipher_value should be a list or tuple'
            secret_text,iv=base64.b64decode(secret),'\0'*16
        if self.set_aes_key():
            if is_encoded:
                secret_text=base64.b64decode(secret_text)
                iv=base64.b64decode(iv)
            cipher=self._build_aes_cipher(self.aes_key, iv, self.DEC)
            v=cipher.update(secret_text)
            v=v+cipher.final()
            del cipher
            retval = v.replace('\x00', '')
        return retval
    
    def aes_encrypt(self, plaintext):            
        """ Encrypt with AES, but fail if aes_key unavailable.
        Important to not allow any data to be saved if the keys are not available
        Returns a tuple of (secret,iv)"""
        if not self.set_aes_key():
            # must FAIL here if key not available and user is trying to save data
            raise ImproperlyConfigured('AES key not available, unable to encrypt sensitive data using the AES algorithm.')
        if self.is_encrypted(plaintext):
            raise ValueError('Attempt to aes encrypt an already encrypted value.')
        iv=os.urandom(16)
        cipher=self._build_aes_cipher(self.aes_key, iv, self.ENC)
        v=cipher.update(plaintext)
        v=v+cipher.final()
        del cipher
        return (v,iv)

    def _build_aes_cipher(self, key, iv, op=ENC):
        return EVP.Cipher(alg='aes_128_cbc', key=key, iv=iv, op=op)
    
    def is_encrypted(self, value, prefix=hash_prefix):
        """ The value string is considered encrypted if it starts with 'self.hash_prefix' or whichever prefix is passed"""
        if not value:
            retval=False
        else:
            if value==prefix:
                raise TypeError('Expected a string value, got just the encryption prefix.')
            if value.startswith(prefix):
                retval=True
            else:
                retval=False
        return retval
    
    def mask_encrypted(self, value, mask='<encrypted>'):
        """ help format values for display by masking them if encrypted at the time of display"""
        if self.is_encrypted(value):
            return mask
        else:
            return value
    
