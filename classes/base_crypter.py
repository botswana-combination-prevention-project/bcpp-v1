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
        'rsa': {'irreversible': {'public': os.path.join(KEY_PATH, 'user-rsa-irreversible-public.pem'),
                                 'salt': os.path.join(KEY_PATH, 'user-rsa-irreversible-salt.key')},
                'restricted': {'public': os.path.join(KEY_PATH, 'user-rsa-restricted-public.pem'),
                               'private': os.path.join(KEY_PATH, 'user-rsa-restricted-private.pem'),
                               'salt': os.path.join(KEY_PATH, 'user-rsa-restricted-salt.key')},
                'local': {'public': os.path.join(KEY_PATH, 'user-rsa-local-public.pem'),
                         'private': os.path.join(KEY_PATH, 'user-rsa-local-private.pem'),
                         'salt': os.path.join(KEY_PATH, 'user-rsa-local-salt.key')},
                },
        'aes': {'local': {'key': os.path.join(KEY_PATH, 'user-aes-local-key.key'),
                          'salt': os.path.join(KEY_PATH, 'user-aes-local-salt.key')},
                }
       }

    PRELOADED_KEYS = copy.deepcopy(VALID_MODES)
    PRELOADED = False

    def __init__(self, *args, **kwargs):

        self.public_key = None
        self.private_key = None
        self.aes_key = None
        self.encrypted_salt = {}
        self.algorithm = None
        self.mode = None
        self.has_encryption_key = False
        if not kwargs.get('no_preload', False):
            self.preload_all_keys()
        else:
            self.PRELOADED_KEYS = copy.deepcopy(self.VALID_MODES)
        super(BaseCrypter, self).__init__(*args, **kwargs)

    def set_public_key(self, keyfile=None, **kwargs):
        """ Load the rsa public key. """
        algorithm = kwargs.get('algorithm', self.algorithm)
        mode = kwargs.get('mode', self.mode)
        if not self.public_key:
            self.has_encryption_key = False
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
                self.has_encryption_key = True
            else:
                try:
                    self.public_key = RSA.load_pub_key(keyfile)
                    print ('successfully loaded {0} {1} '
                           'public key').format(algorithm, mode)
                    self.has_encryption_key = True
                except:
                    print ('warning: failed to load public '
                           'key {0}.').format(keyfile)
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
                    print ('successfully loaded {0} {1} private '
                           'key').format(algorithm, mode)
                except:
                    # if you need a warning here, do so in the subclass
                    pass
        return self.private_key is not None

    def set_aes_key(self, **kwargs):
        """ Retrieve and decrypt the AES key.

        AES key needs to be decrypted using the \'mode\'-rsa private key """
        algorithm = kwargs.get('algorithm', self.algorithm)
        mode = kwargs.get('mode', self.mode)
        if algorithm != 'aes':
            raise TypeError('Invalid algorithm. Expected \'aes\', Got {0}'.format(algorithm))
        if not self.aes_key:
            self.has_encryption_key = False
            if (self.PRELOADED_KEYS.get(algorithm).get(mode) and
                self.KEY_PATH not in self.PRELOADED_KEYS.get(algorithm).get(mode)):
                self.aes_key = self.PRELOADED_KEYS.get(algorithm).get(mode)
                self.has_encryption_key = True
            else:
                try:
                    f = open(self._get_aes_keyfile(algorithm=algorithm, mode=mode), 'r')
                    secret_key = f.read()
                    f.close()
                    self.aes_key = self.rsa_decrypt(
                                       secret_key, algorithm='rsa',
                                       mode=mode)
                    print 'successfully loaded {0} aes key'.format(mode)
                    self.has_encryption_key = True
                except IOError as e:
                    print ('warning: failed to open {0} aes '
                          'key file {0}. Got {1}').format(mode, self._get_aes_keyfile(algorithm=algorithm, mode=mode), e)
                #except:
                #    print ('warning: failed to load aes '
                #           'key {0}.').format(self._get_aes_keyfile())
        return self.aes_key != None

    #def get_local_rsa_private_keyfile(self):
    #    """Return the rsa local key filename."""
    #    return self.VALID_MODES.get('rsa').get('local').get('private')

    def _get_aes_keyfile(self, **kwargs):
        """ Return the aes key filename."""
        algorithm = kwargs.get('algorithm', self.algorithm)
        mode = kwargs.get('mode', self.mode)
        return self.VALID_MODES.get(algorithm).get(mode).get('key')

    def create_new_rsa_key_pairs(self, suffix=str(datetime.today())):
        """ Create a new rsa key-pair. """
        def _blank_callback(self):
            "Replace the default dashes as output upon key generation"
            return

        for mode, mode_pair in self.VALID_MODES.get('rsa').iteritems():
            # Random seed
            Rand.rand_seed(os.urandom(self.RSA_KEY_LENGTH))
            # Generate key pair
            key = RSA.gen_key(self.RSA_KEY_LENGTH, 65537, _blank_callback)
            # create and save the public key to file
            filename = mode_pair.get('public', None)
            # key.save_pub_key('user-private-local.pem'), e.g if suffix=''
            key.save_pub_key(''.join(filename) + suffix)
            print 'Created new rsa key {0}'.format(filename)

            # create and save the private key to file
            filename = mode_pair.get('private', None)
            # key.save_key('user-private-local.pem'), e.g if suffix=''
            if filename:
                key.save_key(''.join(filename) + suffix, None)
                print 'Created new rsa key {0}'.format(filename)
            self.create_new_salt(suffix=suffix, algorithm='rsa', mode=mode)

    def create_aes_key(self, suffix=str(datetime.today()), key=None):
        """ Create a new key and store it safely in a file by using
        rsa local encryption.

        Filename suffix is added to the filename to avoid overwriting an
        existing key """
        for mode in self.VALID_MODES.get('aes').iterkeys():
            if not key:
                key = os.urandom(16)
            filename = self.VALID_MODES.get('aes').get(mode).get('key') + suffix
            secret_aes_key = self.rsa_encrypt(key, algorithm='rsa', mode=mode)
            f = open(filename, 'w')
            f.write(base64.b64encode(secret_aes_key))
            f.close()
            print 'Created new {0} aes key {1}'.format(mode, filename)
            self.create_new_salt(suffix=suffix, algorithm='aes', mode=mode)

    def rsa_encrypt(self, plaintext, **kwargs):
        """Return an un-encoded secret or fail"""
        if not self.set_public_key(**kwargs):
            # FAIL here if key not available and user is trying to save data
            raise ImproperlyConfigured('RSA key not available, unable to '
                                       'encrypt sensitive data using the RSA algorithm.')
        if self.is_encrypted(plaintext):
            raise ValueError('Attempt to rsa encrypt an already '
                             'encrypted value.')
        return self.public_key.public_encrypt(plaintext, RSA.pkcs1_oaep_padding)

    def rsa_decrypt(self, secret, is_encoded=True, **kwargs):
        """ Return plaintext or secret if the private key is not available.

        Secret is base64 encoded unless 'is_encoded' is false"""
        retval = secret
        if self.set_private_key(**kwargs):
            if is_encoded:
                secret = base64.b64decode(secret)
                retval = self.private_key.private_decrypt(
                              secret, RSA.pkcs1_oaep_padding).replace('\x00', '')
        return retval

    def aes_decrypt(self, secret, is_encoded=True, **kwargs):
        """ AES encrypt using the random iv stored with the secret where
        secret is a tuple (secret_text, sep, iv).

        Will return plaintext or the original secret tuple  """
        algorithm = kwargs.get('algorithm', self.algorithm)
        mode = kwargs.get('mode', self.mode)
        retval = secret
        if isinstance(secret, (list, tuple)):
            #cipher_tuple is (cipher, sep, iv)
            secret_text, iv = secret[0], secret[2]
        else:
            print 'warning: {algorithm} {mode} cipher_value should be a list or tuple'.format(algorithm, mode)
            secret_text, iv = base64.b64decode(secret), '\0' * 16
        if self.set_aes_key(algorithm=algorithm, mode=mode):
            if is_encoded:
                secret_text = base64.b64decode(secret_text)
                iv = base64.b64decode(iv)
            cipher = self._build_aes_cipher(self.aes_key, iv, self.DEC)
            v = cipher.update(secret_text)
            v = v + cipher.final()
            del cipher
            retval = v.replace('\x00', '')
        return retval

    def aes_encrypt(self, plaintext, **kwargs):
        """ Return secret as a tuple (secret,iv) or fail.

        Important to not allow any data to be saved if the keys are
        not available"""
        algorithm = kwargs.get('algorithm', self.algorithm)
        mode = kwargs.get('mode', self.mode)
        if not self.set_aes_key(algorithm=algorithm, mode=mode):
            # FAIL here if key not available and user is trying to save data
            raise ImproperlyConfigured('AES key not available, unable to '
                                       'encrypt sensitive data using the '
                                       'AES algorithm.')
        if self.is_encrypted(plaintext):
            raise ValueError('Attempt to aes encrypt an already '
                              'encrypted value.')
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
                raise TypeError('Expected a string value, got just the '
                                 'encryption prefix.')
            if value.startswith(prefix):
                retval = True
            else:
                retval = False
        return retval

    def preload_all_keys(self):
        """ Force all keys to be loaded into preload dictionary . """

        def _load_key(algorithm, mode=None, key_type=None):
            """ Helper method to load one key for load_all_keys. """
            if algorithm == 'rsa':
                if key_type == 'public':
                    self.set_public_key(algorithm=algorithm, mode=mode)
                    key = self.public_key
                    self.public_key = None
                elif key_type == 'private':
                    self.set_private_key(algorithm=algorithm, mode=mode)
                    key = self.private_key
                    self.private_key = None
                elif key_type == 'salt':
                    self.get_encrypted_salt(algorithm=algorithm, mode=mode)
                    key = self.get_encrypted_salt(algorithm=algorithm, mode=mode)
                else:
                    raise TypeError('Unexpected key type for {algorithm} {mode}.'
                                    'Got {key_type}'.format(algorithm=algorithm, mode=mode, key_type=key_type))
            elif algorithm == 'aes':
                if key_type == 'key':
                    self.set_aes_key(algorithm=algorithm, mode=mode)
                    key = self.aes_key
                    self.aes_key = None
                elif key_type == 'salt':
                    self.get_encrypted_salt(algorithm=algorithm, mode=mode)
                    key = self.get_encrypted_salt(algorithm=algorithm, mode=mode)
                else:
                    raise TypeError('Unexpected key type for {algorithm} {mode}.'
                                    'Got {key_type}'.format(algorithm=algorithm, mode=mode, key_type=key_type))
            else:
                raise TypeError('Unknown algorithm. Got {0}.'.format(algorithm))
            return key

        if not self.PRELOADED:
            for algorithm, mode_dict in self.VALID_MODES.iteritems():
                for mode, key_and_filename in mode_dict.iteritems():
                    for key_type in key_and_filename.iterkeys():
                        self.PRELOADED_KEYS[algorithm][mode][key_type] = _load_key(algorithm,
                                                                                    mode,
                                                                                    key_type)
            self.PRELOADED = True

    def create_new_salt(self, length=12,
                        allowed_chars=('abcdefghijklmnopqrstuvwxyzABCDEFGH'
                                       'IJKLMNOPQRSTUVWXYZ0123456789!@#%^&*'
                                       '()?<>.,[]{}'),
                        suffix=str(datetime.today()),
                        **kwargs):
        algorithm = kwargs.get('algorithm', None)
        mode = kwargs.get('mode', None)
        salt = self.rsa_encrypt(
            self.make_random_salt(length, allowed_chars),
            algorithm='rsa', mode=mode)
        path = '{0}{1}'.format(self.VALID_MODES.get(algorithm).get(mode).get('salt'), suffix)
        f = open(path, 'w')
        f.write(base64.b64encode(salt))
        f.close()
        print 'Created new {0} {1} salt {2}'.format(algorithm, mode, path)
        return base64.b64encode(salt)

    def read_salt_from_file(self, **kwargs):
        algorithm = kwargs.get('algorithm', None)
        mode = kwargs.get('mode', None)
        path = self.VALID_MODES.get(algorithm).get(mode).get('salt')
        try:
            f = open(path, 'r')
            retval = f.read()
            print 'successfully loaded {0} {1} salt'.format(algorithm, mode)
        except:
            print 'warning: failed to load {0} {1} salt {2}.'.format(algorithm, mode, path)
            retval = None
        return retval

    def get_encrypted_salt(self, **kwargs):
        """ This is the encrypted salt (which is what's stored in the file) """
        algorithm = kwargs.get('algorithm', None)
        mode = kwargs.get('mode', None)
        if not self.encrypted_salt:
            if (self.PRELOADED_KEYS.get(algorithm).get(mode).get('salt') and self.KEY_PATH not in
                self.PRELOADED_KEYS.get(algorithm).get(mode).get('salt')):
                self.encrypted_salt = self.PRELOADED_KEYS.get(algorithm).get(mode).get('salt')
            else:
                self.encrypted_salt = self.read_salt_from_file(algorithm=algorithm, mode=mode)
        return self.encrypted_salt

    def mask_encrypted(self, value, mask='<encrypted>'):
        """ Help format values for display by masking them if encrypted
        at the time of display."""
        if self.is_encrypted(value):
            return mask
        else:
            return value
