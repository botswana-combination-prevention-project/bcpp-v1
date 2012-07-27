import os
import base64
import copy
import sys
from M2Crypto import Rand, RSA, EVP

from django.core.exceptions import ImproperlyConfigured
from django.conf import settings

from base_crypter import BaseCrypter


class Crypter(BaseCrypter):
    """ Base class for all classes providing RSA and AES encryption methods."""
    RSA_KEY_LENGTH = 2048
    ENC = 1
    DEC = 0
    #keys folder
    try:
        KEY_PATH = settings.KEY_PATH
    except KeyError:
        KEY_PATH = ''
    # valid algorithms, algorithm modes and the corresponding file
    # names where the keys are stored
    VALID_MODES = {
        # algorithm : {mode: {key:path}}
        'rsa': {'irreversible': {'public': os.path.join(KEY_PATH, 'user-rsa-irreversible-public.pem'),
                                 'salt': os.path.join(KEY_PATH, 'user-rsa-irreversible-salt.key')},
                'restricted': {'public': os.path.join(KEY_PATH, 'user-rsa-restricted-public.pem'),
                               'private': os.path.join(KEY_PATH, 'user-rsa-restricted-private.pem'),
                               'salt': os.path.join(KEY_PATH, 'user-rsa-restricted-salt.key')},
                'local': {'public': os.path.join(KEY_PATH, 'user-rsa-local-public.pem'),
                         'private': os.path.join(KEY_PATH, 'user-rsa-local-private.pem'),
                         'salt': os.path.join(KEY_PATH, 'user-rsa-local-salt.key')},
                'salter': {'public': os.path.join(KEY_PATH, 'user-rsa-salter-public.pem'),
                           'private': os.path.join(KEY_PATH, 'user-rsa-salter-private.pem')},
                },
        'aes': {'local': {'key': os.path.join(KEY_PATH, 'user-aes-local.key'),
                          'salt': os.path.join(KEY_PATH, 'user-aes-local.salt')},
                },
       }

    PRELOADED_KEYS = copy.deepcopy(VALID_MODES)
    IS_PRELOADED = False

    def __init__(self, algorithm, mode, **kwargs):

        self.public_key = None
        self.private_key = None
        self.aes_key = None
        #self.encrypted_salt = None
        self.has_encryption_key = False
        self.algorithm = algorithm
        self.mode = mode
        # check algorithm and mode
        if self.algorithm not in self.VALID_MODES.keys():
            raise KeyError('Invalid algorithm \'{algorithm}\'. '
                           'Must be one of {keys}'.format(algorithm=self.algorithm,
                                                          keys=', '.join(self.VALID_MODES.keys())))
        if (self.mode not in
            self.VALID_MODES.get(self.algorithm).iterkeys()):
            raise KeyError('Invalid mode \'{mode}\' for algorithm {algorithm}.'
                           ' Must be one of {keys}'.format(mode=self.mode, algorithm=self.algorithm,
                                                           keys=', '.join(self.VALID_MODES.get(self.algorithm).keys())))
        if kwargs.get('preload', True):
            if not self.IS_PRELOADED:
                self.preload_all_keys()
        else:
            self.PRELOADED_KEYS = copy.deepcopy(self.VALID_MODES)
        super(Crypter, self).__init__()

    def set_public_key(self, keyfile=None, **kwargs):
        """ Load the rsa public key. """
        algorithm = kwargs.get('algorithm', self.algorithm)
        mode = kwargs.get('mode', self.mode)
        self.public_key = None
        if not keyfile:
            # keyfile not specified, so get the default for this
            # algorithm and mode
            if not algorithm or not mode:
                raise AttributeError('Algorithm and mode must be set \
                                      before attempting to set the \
                                      public key')
            keyfile = (self.VALID_MODES.get(algorithm).get(mode)
                                                     .get('public'))
        if isinstance(self.PRELOADED_KEYS.get(algorithm).get(mode).get('public'), RSA.RSA_pub):
            self.public_key = (self.PRELOADED_KEYS.get(algorithm).get(mode).get('public'))
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
        self.private_key = None
        if not keyfile:
            # keyfile not specified, so get default for algorithm and mode
            if not algorithm or not mode:
                raise AttributeError('Algorithm and mode must be set '
                                     'before attempting to set the '
                                     'private key')
            keyfile = self.VALID_MODES.get(algorithm).get(mode).get('private')
        # either load from IS_PRELOADED or from file
        if isinstance(self.PRELOADED_KEYS.get(algorithm).get(mode).get('private'), RSA.RSA):
            self.private_key = (self.PRELOADED_KEYS.get(algorithm).get(mode).get('private'))
        else:
            try:
                if keyfile:
                    self.private_key = RSA.load_key(keyfile)
                    print ('successfully loaded {0} {1} private '
                           'key').format(algorithm, mode)
            except:
                # if you need a warning here, do so in the subclass
                pass
        return self.private_key is not None

    def set_aes_key(self, **kwargs):
        """ Decrypted and set the AES key using the rsa private key for the given mode."""
        algorithm = kwargs.get('algorithm', self.algorithm)
        mode = kwargs.get('mode', self.mode)
        if algorithm != 'aes':
            raise TypeError('Invalid algorithm. Expected \'aes\', Got {0}'.format(algorithm))
        self.has_encryption_key = False
        if self.PRELOADED_KEYS.get(algorithm).get(mode).get('key') and self.KEY_PATH not in self.PRELOADED_KEYS.get(algorithm).get(mode).get('key'):
            self.aes_key = self.PRELOADED_KEYS.get(algorithm).get(mode).get('key')
        else:
            try:
                path = self.VALID_MODES.get(algorithm).get(mode).get('key')
                f = open(path, 'r')
                encrypted_aes = f.read()
                f.close()
                self.aes_key = self._decrypt_aes_key(encrypted_aes, mode)
                print 'successfully loaded {0} aes key'.format(mode)
            except IOError as e:
                print ('warning: failed to open {0} aes '
                      'key file {0}. Got {1}').format(mode, path, e)
            except RSA.RSAError as e:
                print 'RSA Error: failed to decrypt {0} {1} key from {2}'.format(algorithm, mode, path)
                raise
            except:
                print "Unexpected error:", sys.exc_info()[0]
                raise
        return self.aes_key != None

    #def _get_aes_keyfile(self, **kwargs):
    #    """ Return the aes key filename."""
    #    algorithm = kwargs.get('algorithm', self.algorithm)
    #    mode = kwargs.get('mode', self.mode)
    #    return self.VALID_MODES.get(algorithm).get(mode).get('key')

    def _create_new_rsa_key_pairs(self):
        """ Create a new rsa key-pair. """

        def _blank_callback(self):
            "Replace the default dashes as output upon key generation"
            return
        algorithm = 'rsa'
        for mode, key_pair in self.VALID_MODES.get(algorithm).iteritems():
            # Random seed
            Rand.rand_seed(os.urandom(self.RSA_KEY_LENGTH))
            # Generate key pair
            key = RSA.gen_key(self.RSA_KEY_LENGTH, 65537, _blank_callback)
            # create and save the public key to file
            filename = key_pair.get('public', None)
            if key.save_pub_key(''.join(filename)) > 0:
                print '(*) Created new {0} {1} {2}'.format(algorithm, mode, filename)
            else:
                print '( ) Failed to create new {0} {1} {2}'.format(algorithm, mode, filename)
            # create and save the private key to file
            filename = key_pair.get('private', None)
            # key.save_key('user-private-local.pem'), e.g if suffix=''
            if filename:
                if key.save_key(''.join(filename), None) > 0:
                    print '(*) Created new {0} {1} key {2}'.format(algorithm, mode, filename)
                else:
                    print '( ) Failed to create new {0} {1} key {2}'.format(algorithm, mode, filename)

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
            retval = self.private_key.private_decrypt(secret, RSA.pkcs1_oaep_padding).replace('\x00', '')
        return retval

    def _create_new_aes_keys(self, key=None):
        """ Create a new key and store it safely in a file by using rsa encryption for the mode.

        Filename suffix is added to the filename to avoid overwriting an
        existing key """
        algorithm = 'aes'
        for mode in self.VALID_MODES.get(algorithm).iterkeys():
            if not key:
                key = os.urandom(16)
            path = self.VALID_MODES.get(algorithm).get(mode).get('key')
            encrypted_aes = self._encrypt_aes_key(key, mode)
            if os.path.exists(path):
                print ('( ) Failed to create new {0} {1} key. File exists. {2}'.format(algorithm, mode, path))
            else:
                f = open(path, 'w')
                f.write(base64.b64encode(encrypted_aes))
                f.close()
                print '(*) Created new {0} {1} key {2}'.format(algorithm, mode, path)

    def aes_decrypt(self, secret, is_encoded=True, **kwargs):
        """ AES decrypt a value using the random iv stored with the secret where
        secret is a tuple (secret_text, sep, iv).

        Will return plaintext or the original secret tuple  """
        algorithm = kwargs.get('algorithm', self.algorithm)
        mode = kwargs.get('mode', self.mode)
        retval = secret
        if secret:
            #cipher_tuple is (cipher, sep, iv)
            if isinstance(secret, (basestring)):
                print ('warning: decrypt {algorithm} {mode} expects secret to be a list or tuple. '
                      'Got basestring').format(algorithm=algorithm, mode=mode)
                secret_text, iv = secret, '\0' * 16
            try:
                secret_text, iv = secret[0], secret[2]
            except IndexError:
                secret_text, iv = secret[0], secret[1]
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
        retval = plaintext
        if plaintext:
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
            retval = map(base64.b64encode, (v, iv))
        return retval

    def _build_aes_cipher(self, key, iv, op=ENC):
        return EVP.Cipher(alg='aes_128_cbc', key=key, iv=iv, op=op)

    def _decrypt_aes_key(self, encrypted_aes, mode):
        public_key = copy.copy(self.public_key)
        plain_aes = self.rsa_decrypt(encrypted_aes, algorithm='rsa', mode=mode)
        self.public_key = public_key
        return plain_aes

    def _encrypt_aes_key(self, plain_aes, mode):
        private_key = copy.copy(self.private_key)
        encrypted_aes = self.rsa_encrypt(plain_aes, algorithm='rsa', mode=mode)
        self.private_key = private_key
        return encrypted_aes

    def preload_all_keys(self):
        """ Force all keys to be loaded into preload dictionary . """

        def load_key(algorithm, mode=None, key_name=None):
            """ Helper method to load one key for load_all_keys. """
            if algorithm == 'rsa':
                if key_name == 'public':
                    self.set_public_key(algorithm=algorithm, mode=mode)
                    key = self.public_key
                    self.public_key = None
                elif key_name == 'private':
                    self.set_private_key(algorithm=algorithm, mode=mode)
                    key = self.private_key
                    self.private_key = None
                elif key_name == 'salt':
                    key = self.get_encrypted_salt(algorithm, mode)
                else:
                    raise TypeError('Unexpected key type for {algorithm} {mode}.'
                                    'Got {key_name}'.format(algorithm=algorithm, mode=mode, key_name=key_name))
            elif algorithm == 'aes':
                if key_name == 'key':
                    self.set_aes_key(algorithm=algorithm, mode=mode)
                    key = self.aes_key
                    self.aes_key = None
                elif key_name == 'salt':
                    key = self.get_encrypted_salt(algorithm, mode)
                else:
                    raise TypeError('Unexpected key type for {algorithm} {mode}.'
                                    'Got {key_name}'.format(algorithm=algorithm, mode=mode, key_name=key_name))
            else:
                raise TypeError('Unknown algorithm. Got {0}.'.format(algorithm))
            return key

        if not self.is_preloaded_with_keys():
            print 'Preloading keys ...'
            for algorithm, mode_dict in self.VALID_MODES.iteritems():
                for mode, key_dict in mode_dict.iteritems():
                    for key_name in key_dict.iterkeys():
                        self.PRELOADED_KEYS[algorithm][mode][key_name] = load_key(algorithm, mode, key_name)
            # are all keys preloaded now?
            if self.is_preloaded_with_keys('warning: failed to preload {algorithm} {mode} {key_name}'):
                # run some tests
                self.test()
                print 'Done preloading keys.'
            else:
                print 'No keys found to load.'
            return True

    def _create_new_salts(self, length=12,
                        allowed_chars='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#%^&*()?<>.,[]{}'):
        """ Creates a new salt and encrypts it with the \'salter\' rsa public key.

        Algorithm and mode are needed to get the filename from VAILD_MODES.
        """
        # create a salt for each algorithm and mode
        for algorithm, mode_dict in self.VALID_MODES.iteritems():
            for mode in mode_dict.iterkeys():
                if self.VALID_MODES.get(algorithm).get(mode).get('salt'):
                    path = self.VALID_MODES.get(algorithm).get(mode).get('salt')
                    salt = self._encrypt_salt(self.make_random_salt(length, allowed_chars))
                    f = open(path, 'w')
                    f.write(base64.b64encode(salt))
                    f.close()
                    print '(*) Created new {0} {1} salt {2}'.format(algorithm, mode, path)

    def _encrypt_salt(self, plain_salt):
        """Encrypts a given salt using the 'salter' rsa key pair """
        #public_key = copy.copy(self.public_key)
        encrypted_salt = self.rsa_encrypt(plain_salt, algorithm='rsa', mode='salter')
        #self.public_key = public_key
        return encrypted_salt

    def _decrypt_salt(self, encrypted_salt):
        """Decrypts a given salt using the 'salter' rsa key pair """
        #public_key = copy.copy(self.public_key)
        plain_salt = self.rsa_decrypt(encrypted_salt, algorithm='rsa', mode='salter')
        #self.public_key = public_key
        return plain_salt

    def _read_encrypted_salt_from_file(self, **kwargs):
        algorithm = kwargs.get('algorithm', None)
        mode = kwargs.get('mode', None)
        path = self.VALID_MODES.get(algorithm).get(mode).get('salt')
        try:
            f = open(path, 'r')
            encrypted_salt = f.read()
            print 'successfully loaded {0} {1} salt from file'.format(algorithm, mode)
        except:
            print 'warning: failed to load {0} {1} salt {2} from file'.format(algorithm, mode, path)
            encrypted_salt = None
        return encrypted_salt

    def get_encrypted_salt(self, algorithm, mode):
        """ Sets and returns the encrypted_salt for the given algorithm and mode.

        Gets from PRELOADED_KEYS or reads from the file but will always reset it."""
        if (self.PRELOADED_KEYS.get(algorithm).get(mode).get('salt') and
                self.KEY_PATH not in self.PRELOADED_KEYS.get(algorithm).get(mode).get('salt')):
            encrypted_salt = self.PRELOADED_KEYS.get(algorithm).get(mode).get('salt')
        else:
            encrypted_salt = self._read_encrypted_salt_from_file(algorithm=algorithm, mode=mode)
        return encrypted_salt

    def get_key_paths(self):
        """ Returns a list of key pathnames """
        paths = []
        for algorithm, mode_dict in self.VALID_MODES.iteritems():
            for mode, key_dict in mode_dict.iteritems():
                for key_name in key_dict.iterkeys():
                    if self.VALID_MODES.get(algorithm).get(mode).get(key_name):
                        paths.append(self.VALID_MODES.get(algorithm).get(mode).get(key_name))
        return paths

    def is_preloaded_with_keys(self, msg=None):
        """ Checks if keys are preloaded and returns False on the first missing key.

        If msg is passed, will run through all keys displaying a message for each
        missing key."""
        preloaded = True
        for algorithm, mode_dict in self.VALID_MODES.iteritems():
            for mode, key_dict in mode_dict.iteritems():
                for key_name in key_dict.iterkeys():
                    if not isinstance(self.PRELOADED_KEYS[algorithm][mode][key_name], (RSA.RSA_pub, RSA.RSA, basestring)):
                        preloaded = False
                        if msg:
                            print msg.format(algorithm=algorithm, mode=mode, key_name=key_name)
                        else:
                            break
                    elif isinstance(self.PRELOADED_KEYS[algorithm][mode][key_name], basestring):
                        if self.KEY_PATH in self.PRELOADED_KEYS[algorithm][mode][key_name]:
                            preloaded = False
                            if msg:
                                print msg.format(algorithm=algorithm, mode=mode, key_name=key_name)
                            else:
                                break
                    else:
                        pass
        return preloaded

    def test(self):

        def _encrypt(self, plaintext, algorithm, mode):
            try:
                if algorithm == 'rsa':
                    encrypted_text = self.rsa_encrypt(plaintext, algorithm=algorithm, mode=mode)
                elif algorithm == 'aes':
                    encrypted_text = self.aes_encrypt(plaintext, algorithm=algorithm, mode=mode)
                else:
                    raise TypeError('Encryption error for {0}'.format(algorithm))
            except TypeError as e:
                print 'Encrypt error for {0} {1}. Got \'{2}\''.format(algorithm, mode, e)
                encrypted_text = None
                pass
            return encrypted_text

        def _decrypt(self, encrypted_text, algorithm, mode):
            try:
                if algorithm == 'rsa':
                    plaintext = self.rsa_decrypt(encrypted_text, False, algorithm=algorithm, mode=mode)
                elif algorithm == 'aes':
                    plaintext = self.aes_decrypt(encrypted_text, algorithm=algorithm, mode=mode)
                else:
                    raise TypeError('Encryption error for {0}'.format(algorithm))
            except TypeError as e:
                print 'Decrypt error for {0} {1}. Got \'{2}\''.format(algorithm, mode, e)
                plaintext = None
                pass
            return plaintext

        plaintext = '123456789ABCDEFG'
        for algorithm, mode_dict in self.VALID_MODES.iteritems():
            for mode in mode_dict.iterkeys():
                #print 'Testing {algorithm} {mode}...'.format(algorithm=algorithm, mode=mode)
                encrypted_text = _encrypt(self, plaintext, algorithm, mode)
                decrypted_text = _decrypt(self, encrypted_text, algorithm, mode)
                if encrypted_text == decrypted_text and decrypted_text is not None:
                    decrypted_text = base64.b64encode(decrypted_text)
                if decrypted_text != plaintext:
                    print '( ) Encrypt/Decrypt failed for {algorithm} {mode}.'.format(algorithm=algorithm, mode=mode)
                else:
                    print '(*) Encrypt/Decrypt works for {algorithm} {mode}'.format(algorithm=algorithm, mode=mode)

    def create_new_keys(self):
        self._create_new_rsa_key_pairs()
        self._create_new_salts()
        self._create_new_aes_keys()
