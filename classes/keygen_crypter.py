import os
import base64
from M2Crypto import Rand, RSA, EVP

from crypter import Crypter


class KeygenCrypter(Crypter):

    def create_new_keys(self):
        self._create_new_rsa_key_pairs()
        self._create_new_salts()
        self._create_new_aes_keys()

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
