import hashlib
from django.conf import settings


class Hasher(object):
    
    def __init__(self, *args, **kwargs):
        self.salt = settings.SALT
        self.length = 64
        
    def get_hash(self, value, salt=None):
        if not value:
            retval = None
        else:
            # only change algorithm if existing hashes have been updated
            if not salt:
                salt = self.salt
            if not isinstance(salt, str):
                raise TypeError('Hasher expects \'salt\' to be a string.')
            hlib = hashlib.sha256()
            hlib.update(salt)
            hlib.update(value)
            hash_value = hlib.hexdigest()
            retval = hash_value
            #if len(hash_value) != self.length:
            #    raise TypeError('Invalid hash_text length, expected %s. Got %s' % (self.length, len(hash_value)))
        return retval