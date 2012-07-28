import base64

from django.db.models import get_model

from crypter import Crypter
from hasher import Hasher


class FieldCrypter(object):

    """ Subclass to be used with models that expect to stored just the hash and for this class to handle the secret. """

    def __init__(self, algorithm, mode):

        self.algorithm = algorithm
        self.mode = mode
        self.crypter = Crypter(algorithm=algorithm, mode=mode)
        self.hasher = Hasher(algorithm=algorithm, mode=mode)

    def encrypt(self, value, **kwargs):
        """ Return the encrypted field value (hash+secret) where secret is secret or secret+secret_iv. """
        if not value:
            hash_secret = value   # value is None
        else:
            if not self.is_encrypted(value):
                if self.algorithm == 'aes':
                    encoded_secret = self.crypter.IV_PREFIX.join(self.crypter.aes_encrypt(value))
                elif self.algorithm == 'rsa':
                    if len(value) >= self.crypter.RSA_KEY_LENGTH / 24:
                        raise ValueError('String value to encrypt may not exceed {0} characters. '
                                         'Got {1}.'.format(self.crypter.RSA_KEY_LENGTH / 24, len(value)))
                    secret = self.crypter.rsa_encrypt(value)
                    encoded_secret = base64.b64encode(secret)
                else:
                    raise ValueError('Cannot determine algorithm to use for encryption. Valid options are {0}. Got {1}'.format(', '.join(self.crypter.VALID_MODES.keys()), self.algorithm))
                hashed_value = self.get_hash(value)
                hash_secret = self.crypter.HASH_PREFIX + hashed_value + self.crypter.SECRET_PREFIX + encoded_secret
            else:
                hash_secret = value  # value did not change
        return hash_secret

    def decrypt(self, secret, secret_is_hash=True, **kwargs):
        """ Decrypt secret and if secret is a hash, use hash to lookup the real secret first.

        Do not assume secret is an encrypted value, look for HASH_PREFIX or secret prefix.
        By default we expect secret to be the stored field value -- which is a hash.
        If we use this method for a secret that is not a hash, then the prefix is
        the SECRET_PREFIX and the lookup step is skipped. """

        plaintext = secret
        if secret:
            prefix = lambda x: self.crypter.HASH_PREFIX if x else self.crypter.SECRET_PREFIX
            if self.is_encrypted(secret, prefix(secret_is_hash)):
                if secret_is_hash:
                    hashed_value = self.get_hash(secret)
                    secret = self._get_secret_from_hash_secret(secret, hashed_value)
                else:
                    secret = secret[len(self.crypter.SECRET_PREFIX):]  # secret is not a hash
                if secret:
                    if self.algorithm == 'aes':
                        if self.crypter.set_aes_key():
                            plaintext = self.crypter.aes_decrypt(secret.partition(self.crypter.IV_PREFIX))
                    elif self.algorithm == 'rsa':
                        if self.crypter.set_private_key():
                            plaintext = self.crypter.rsa_decrypt(secret)
                    else:
                        raise ValueError('Cannot determine algorithm for decryption.'
                                         ' Valid options are {0}. Got {1}'.format(', '.join(self.crypter.VALID_MODES.keys()),
                                                                                  self.algorithm))
                else:
                    raise ValueError('When decrypting from hash, could not find secret'
                                     ' in lookup for hash {0}'.format(hashed_value))
        return plaintext

    def is_encrypted(self, value, prefix=None):
        return self.crypter.is_encrypted(value, prefix)

    def update_secret_in_lookup(self, hash_secret):
        """ Given a hash+secret string, updates lookup with hashed_value and secret pairs """
        hashed_value = None
        if hash_secret:
            # get and update or create the crypt model with this hash, cipher pair
            hashed_value = self.get_hash(hash_secret)
            secret = self._get_secret_from_hash_secret(hash_secret, hashed_value)
            Crypt = get_model('bhp_crypto', 'crypt')
            if Crypt.objects.filter(hash=hashed_value):
                if secret:
                    crypt = Crypt.objects.get(hash=hashed_value)
                    crypt.secret = secret
                    crypt.save()
            else:
                if secret:
                    Crypt.objects.create(hash=hashed_value,
                                         secret=secret,
                                         algorithm=self.algorithm,
                                         mode=self.mode)
                else:
                    # if the hash is not in the crypt model and you do not have a secret
                    # update: if performing a search, instead of data entry, the hash will not
                    # exist, so this print should eventually be removed
                    print 'hash not found in crypt model. {0} {1} {2}'.format(self.algorithm, self.mode, hashed_value)

    def get_hash(self, value):
        """ Returns the hashed value without hash_prefix by either splitting it from value or hashing value."""
        if self.is_encrypted(value):
            # if value is an encrypted value string, split to get hashed_value segment (less hash_prefix ans secret)
            hashed_value = value[len(self.crypter.HASH_PREFIX):][:self.hasher.length]
        else:
            encrypted_salt = self.crypter.get_encrypted_salt(self.algorithm, self.mode)
            hashed_value = self.hasher.get_hash(value, self.algorithm, self.mode, self.crypter._decrypt_salt(encrypted_salt))
        return hashed_value

    def get_hash_with_prefix(self, value):
        if value:
            retval = self.crypter.HASH_PREFIX + self.get_hash(value)
        else:
            retval = None
        return retval

    def get_prep_value(self, encrypted_value, value, **kwargs):
        """ Gets the hash from encrypted value for the DB """
        update_lookup = kwargs.get('update_lookup', True)
        if encrypted_value != value:
            # encrypted_value is a hashed_value + secret, use this to put the secret into the lookup for this hashed_value.
            if update_lookup:
                self.update_secret_in_lookup(encrypted_value)
        hashed_value = self.get_hash(encrypted_value)
        return self.crypter.HASH_PREFIX + hashed_value

    def _get_secret_from_hash_secret(self, value, hashed_value):
        """ Returns the secret by splitting value on the hashed_value if value is hash+secret otherwise value is the prefix+hashed_value. """
        if not value:
            retval = None
        else:
            if self.is_encrypted(value):
                # split on hash, but if this is a hash only, secret_string will be None
                secret = value[len(self.crypter.HASH_PREFIX) + len(hashed_value) + len(self.crypter.SECRET_PREFIX):]
                if not secret:
                    # lookup secret_string for this hashed_value
                    secret = self._lookup_secret(hashed_value)
                    if not secret:
                        raise ValueError('Could not retrieve a secret for given hash. Got {0}'.format(hashed_value))
                retval = secret
            else:
                raise ValueError('Value must be encrypted or None.')
        return retval

    def _lookup_secret(self, hashed_value):
        """ Looks up a secret for hashed+value in the Crypt model.

        If not found, returns None"""
        Crypt = get_model('bhp_crypto', 'crypt')
        if Crypt.objects.filter(hash=hashed_value):
            crypt = Crypt.objects.get(hash=hashed_value)
            ret_val = crypt.secret
        else:
            ret_val = None
        return ret_val
