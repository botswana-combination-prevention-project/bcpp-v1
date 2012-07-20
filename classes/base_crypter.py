import os
import base64
import copy
from datetime import datetime
from M2Crypto import Rand, RSA, EVP

from django.core.exceptions import ImproperlyConfigured
from django.conf import settings

from base import Base


class BaseCrypter(Base):
    """ Base class for all classes providing RSA and AES encryption methods."""
    RSA_KEY_LENGTH = 2048
    ENC = 1
    DEC = 0
    # prefix for each segment of an encrypted value, also used to calculate
    # field length for model.
    HASH_PREFIX = 'enc1:::'  # uses a prefix to flag as encrypted
    SECRET_PREFIX = 'enc2:::'  # like django-extensions does
    IV_PREFIX = 'iv:::'
    #keys folder
    try:
        KEY_PATH = settings.KEY_PATH
    except KeyError:
        KEY_PATH = ''
    # valid algorithms, algorithm modes and the corresponding file
    # names where the keys are stored
    VALID_MODES = {
        'rsa': {'irreversible-rsa': {'public':
                                     os.path.join(KEY_PATH, 'user-public-irreversible.pem')},
                'restricted-rsa': {'public':
                                   os.path.join(KEY_PATH, 'user-public-restricted.pem'),
                                   'private':
                                   os.path.join(KEY_PATH, 'user-private-restricted.pem')},
                'local-rsa': {'public':
                              os.path.join(KEY_PATH, 'user-public-local.pem'),
                             'private': os.path.join(KEY_PATH, 'user-private-local.pem')},
                },
        'aes': {'local-aes': os.path.join(KEY_PATH, 'user-aes-local')},
        'salt': os.path.join(KEY_PATH, 'user-encrypted-salt')
    }

    PRELOADED_KEYS = copy.deepcopy(VALID_MODES)
    PRELOADED = False

    def __init__(self, *args, **kwargs):

        self.public_key = None
        self.private_key = None
        self.aes_key = None
        self.encrypted_salt = None
        self.algorithm = None
        self.mode = None
        self.preload_all_keys()
        super(BaseCrypter, self).__init__(*args, **kwargs)

    def set_public_key(self, keyfile=None, **kwargs):
        """ Load the rsa public key. """
        algorithm = kwargs.get('algorithm', self.algorithm)
        mode = kwargs.get('mode', self.mode)
        if not self.public_key:
            if not keyfile:
                # keyfile not specified, so get the default for this
                # algorithm and mode
                if not algorithm or not mode:
                    raise AttributeError('Algorithm and mode must be set \
                                          before attempting to set the \
                                          public key')
                keyfile = (self.VALID_MODES.get(algorithm).get(mode)
                                                         .get('public'))
            if isinstance(
                self.PRELOADED_KEYS.get(algorithm).get(mode)
                                             .get('public'), RSA.RSA_pub):
                self.public_key = (self.PRELOADED_KEYS.get(algorithm)
                                                     .get(mode).get('public'))
            else:
                try:
                    self.public_key = RSA.load_pub_key(keyfile)
                    print 'successfully loaded {0} {1} \
                           public key'.format(algorithm, mode)
                except:
                    print 'warning: failed to load public \
                           key {0}.'.format(keyfile)
        return self.public_key is not None

    def set_private_key(self, keyfile=None, **kwargs):
        """ Load the rsa private key. """
        algorithm = kwargs.get('algorithm', self.algorithm)
        mode = kwargs.get('mode', self.mode)
        if not self.private_key:
            if not keyfile:
                # keyfile not specified, so get default for algorithm and mode
                if not algorithm or not mode:
                    raise AttributeError('Algorithm and mode must be set '
                                         'before attempting to set the '
                                         'private key')
                keyfile = (
                    self.VALID_MODES.get(algorithm).get(mode).get('private'))
            # either load from PRELOADED or from file
            if isinstance(self.PRELOADED_KEYS.get(algorithm).get(
                              mode).get('private'), RSA.RSA):
                self.private_key = (
                    self.PRELOADED_KEYS.get(algorithm).get(
                        mode).get('private'))
            else:
                try:
                    self.private_key = RSA.load_key(keyfile)
                    print 'successfully loaded {0} {1} private \
                           key'.format(algorithm, mode)
                except:
                    # if you need a warning here, do so in the subclass
                    pass
        return self.private_key is not None

    def set_aes_key(self):
        """ Retrieve and decrypt the AES key. """
        if not self.aes_key:
            if (self.PRELOADED_KEYS.get('aes').get('local-aes') and
                self.KEY_PATH not in
                self.PRELOADED_KEYS.get('aes').get('local-aes')):
                self.aes_key = self.PRELOADED_KEYS.get('aes').get('local-aes')
            else:
                try:
                    f = open(self._get_aes_keyfile(), 'r')
                    secret_key = f.read()
                    f.close()
                    self.aes_key = self.rsa_decrypt(
                                       secret_key, algorithm='rsa',
                                       mode='local-rsa')
                    print 'successfully loaded aes key'
                except:
                    print 'warning: failed to load aes \
                           key {0}.'.format(self._get_aes_keyfile())
        return self.aes_key != None

    def get_local_rsa_private_keyfile(self):
        """Return the local-rsa key filename."""
        return self.VALID_MODES.get('rsa').get('local-rsa').get('private')

    def _get_aes_keyfile(self):
        """ Return the aes key filename."""
        return self.VALID_MODES.get('aes').get('local-aes')

    def create_new_rsa_key_pairs(self, suffix=str(datetime.today())):
        """ Create a new rsa key-pair. """
        def _blank_callback(self):
            "Replace the default dashes as output upon key generation"
            return

        for mode_pair in self.VALID_MODES.get('rsa').itervalues():
            # Random seed
            Rand.rand_seed(os.urandom(self.RSA_KEY_LENGTH))
            # Generate key pair
            key = RSA.gen_key(self.RSA_KEY_LENGTH, 65537, _blank_callback)
            # create and save the public key to file
            filename = mode_pair.get('public', None)
            # key.save_pub_key('user-private-local.pem'), e.g if suffix=''
            key.save_pub_key(''.join(filename) + suffix)
            # create and save the private key to file
            filename = mode_pair.get('private', None)
            # key.save_key('user-private-local.pem'), e.g if suffix=''
            if filename:
                key.save_key(''.join(filename) + suffix, None)

    def create_aes_key(self, suffix=str(datetime.today()), key=None):
        """ Create a new key and store it safely in a file by using
        local-rsa-encryption.

        Filename suffix is added to the filename to avoid overwriting an
        existing key """
        if not key:
            key = os.urandom(16)
        # check if public key is set
        if not self.public_key:
            self.set_public_key(self.VALID_MODES.get('rsa').get('local-rsa').get('public'))
        filename = self.VALID_MODES.get('aes').get('local-aes') + suffix
        secret_aes_key = self.rsa_encrypt(key, algorithm='rsa', mode='local-rsa')
        f = open(filename, 'w')
        f.write(base64.b64encode(secret_aes_key))
        f.close()

    def rsa_encrypt(self, plaintext, **kwargs):
        """Return an un-encoded secret or fail"""
        if not self.set_private_key(**kwargs):
            # FAIL here if key not available and user is trying to save data
            raise ImproperlyConfigured('RSA key not available, unable to \
                            encrypt sensitive data using the RSA algorithm.')
        if self.is_encrypted(plaintext):
            raise ValueError('Attempt to rsa encrypt an already \
                              encrypted value.')
        return self.public_key.public_encrypt(plaintext, RSA.pkcs1_oaep_padding)

    def rsa_decrypt(self, secret, is_encoded=True, **kwargs):
        """ Return plaintext or secret if the private key is not available.

        Secret is base64 encoded unless 'is_encoded' is false"""
        retval = secret
        if self.set_private_key(**kwargs):
            if is_encoded:
                secret = base64.b64decode(secret)
            retval = (self.private_key.private_decrypt(
                          secret, RSA.pkcs1_oaep_padding).replace('\x00', ''))
        return retval

    def aes_decrypt(self, secret, is_encoded=True):
        """ AES encrypt using the random iv stored with the secret where
        secret is a tuple (secret_text, sep, iv).

        Will return plaintext or the original secret tuple  """
        retval = secret
        if isinstance(secret, (list, tuple)):
            #cipher_tuple is (cipher, sep, iv)
            secret_text, iv = secret[0], secret[2]
        else:
            print 'warning: aes cipher_value should be a list or tuple'
            secret_text, iv = base64.b64decode(secret), '\0' * 16
        if self.set_aes_key():
            if is_encoded:
                secret_text = base64.b64decode(secret_text)
                iv = base64.b64decode(iv)
            cipher = self._build_aes_cipher(self.aes_key, iv, self.DEC)
            v = cipher.update(secret_text)
            v = v + cipher.final()
            del cipher
            retval = v.replace('\x00', '')
        return retval

    def aes_encrypt(self, plaintext):
        """ Return secret as a tuple (secret,iv) or fail.

        Important to not allow any data to be saved if the keys are
        not available"""
        if not self.set_aes_key():
            # FAIL here if key not available and user is trying to save data
            raise ImproperlyConfigured('AES key not available, unable to \
                                        encrypt sensitive data using the \
                                        AES algorithm.')
        if self.is_encrypted(plaintext):
            raise ValueError('Attempt to aes encrypt an already \
                              encrypted value.')
        iv = os.urandom(16)
        cipher = self._build_aes_cipher(self.aes_key, iv, self.ENC)
        v = cipher.update(plaintext)
        v = v + cipher.final()
        del cipher
        return (v, iv)

    def _build_aes_cipher(self, key, iv, op=ENC):
        return EVP.Cipher(alg='aes_128_cbc', key=key, iv=iv, op=op)

    def is_encrypted(self, value, prefix=HASH_PREFIX):
        """ The value string is considered encrypted if it starts
        with 'self.HASH_PREFIX' or whichever prefix is passed."""
        if not value:
            retval = False
        else:
            if value == prefix:
                raise TypeError('Expected a string value, got just the \
                                 encryption prefix.')
            if value.startswith(prefix):
                retval = True
            else:
                retval = False
        return retval

    def preload_all_keys(self):
        """ Force all keys to be loaded into preload dictionary . """

        def _load_key(algorithm, mode=None, key_pair_type=None):
            """ Helper method to load one key for load_all_keys. """
            if algorithm == 'rsa':
                if key_pair_type == 'public':
                    self.set_public_key(algorithm=algorithm, mode=mode)
                    key = self.public_key
                    self.public_key = None
                elif key_pair_type == 'private':
                    self.set_private_key(algorithm=algorithm, mode=mode)
                    key = self.private_key
                    self.private_key = None
            elif algorithm == 'aes':
                self.set_aes_key()
                key = self.aes_key
                self.aes_key = None
            elif algorithm == 'salt':
                key = self.get_encrypted_salt()
            else:
                raise TypeError('Unknown algorithm. \
                                 Got {0}.'.format(algorithm))
            return key

        if not self.PRELOADED:
            for algorithm, mode_dict in self.VALID_MODES.iteritems():
                if not isinstance(mode_dict, dict):
                    self.PRELOADED_KEYS[algorithm] = _load_key(algorithm)
                else:
                    for mode, val in mode_dict.iteritems():
                        if not isinstance(val, dict):
                            self.PRELOADED_KEYS[algorithm][mode] = _load_key(algorithm, mode)
                        else:
                            for key_pair_type in val.iterkeys():
                                self.PRELOADED_KEYS[
                                    algorithm][mode][key_pair_type] = _load_key(algorithm,
                                                                                mode,
                                                                                key_pair_type)
            self.PRELOADED = True

    def create_new_salt(self, length=12,
                        allowed_chars='abcdefghijklmnopqrstuvwxyzABCDEFGH\
                                       IJKLMNOPQRSTUVWXYZ0123456789!@#%^&*\
                                       ()?<>.,[]{}',
                        suffix=str(datetime.today())):
        if not self.public_key:
            self.set_public_key(
                self.VALID_MODES.get('rsa').get('local-rsa').get('public'))
        salt = self.rsa_encrypt(
            self.make_random_salt(length, allowed_chars),
            algorithm='rsa', mode='local-rsa')
        path = '{0}{1}'.format(self.VALID_MODES.get('salt'), suffix)
        f = open(path, 'w')
        f.write(base64.b64encode(salt))
        f.close()
        return base64.b64encode(salt)

    def read_salt_from_file(self):
        path = self.VALID_MODES.get('salt')
        try:
            f = open(path, 'r')
            retval = f.read()
            print 'successfully loaded salt'
        except:
            print 'warning: failed to load salt {0}.'.format(path)
            retval = None
        return retval

    def get_encrypted_salt(self):
        """ This is the encrypted salt (which is what's stored in the file) """
        if not self.encrypted_salt:
            if (self.PRELOADED_KEYS.get('salt') and self.KEY_PATH not in
                self.PRELOADED_KEYS.get('salt')):
                self.encrypted_salt = self.PRELOADED_KEYS.get('salt')
            else:
                self.encrypted_salt = self.read_salt_from_file()
        return self.encrypted_salt

    def mask_encrypted(self, value, mask='<encrypted>'):
        """ Help format values for display by masking them if encrypted
        at the time of display."""
        if self.is_encrypted(value):
            return mask
        else:
            return value
