import hashlib

from django.core.exceptions import ValidationError

from base_crypter import BaseCrypter


class Hasher(BaseCrypter):
    """ handle all hashing """
    def __init__(self, *args, **kwargs):
        self.length = self._get_hash_length()
        self.iterations = 40
        super(Hasher, self).__init__(*args, **kwargs)

    def new_hasher(self, value=''):
        return hashlib.sha256(value)

    def get_salt(self, **kwargs):
        algorithm = kwargs.get('algorithm', None)
        mode = kwargs.get('mode', None)
        self.encrypted_salt = self.set_encrypted_salt(algorithm=algorithm, mode=mode)
        return self._decrypt_salt(self.encrypted_salt)

    def _get_hash_length(self):
        return hashlib.sha256('Foo').block_size

    def get_hash(self, value, **kwargs):
        """ for a given value, return a salted SHA256 hash """
        algorithm = kwargs.get('algorithm', None)
        mode = kwargs.get('mode', None)
        if not value:
            retval = None
        else:
            salt = self.get_salt(algorithm=algorithm, mode=mode)
            if not isinstance(salt, str):
                raise ValidationError('The Encryption keys are not available '
                                      'to this system. Unable to save '
                                      'sensitive data.')
            digest = self.new_hasher(salt + value).digest()
            # iterate
            for x in range(0, self.iterations - 1):
                digest = self.new_hasher(digest).digest()
            hash_value = digest.encode("hex")
            retval = hash_value
        return retval
