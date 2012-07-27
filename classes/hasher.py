import hashlib

from django.core.exceptions import ValidationError

#from base_crypter import BaseCrypter


class Hasher(object):
    """ handle all hashing """
    def __init__(self, *args, **kwargs):
        self.length = self._get_hash_length()
        self.iterations = 40
        #super(Hasher, self).__init__(*args, **kwargs)

    def new_hasher(self, value=''):
        # encode as utf-8 to avoid UnicodeEncodeError.
        # for example: 'ascii' codec can't encode character u'\xb4' in position 60:
        # ordinal not in range(128)
        return hashlib.sha256(value.encode('utf-8'))

    def _get_hash_length(self):
        return hashlib.sha256('Foo').block_size

    def get_hash(self, value, algorithm, mode, salt):
        """ for a given value, return a salted SHA256 hash """
        if not value:
            retval = None
        else:
            #salt = self.get_salt(algorithm, mode, _decrypt_salt)
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
