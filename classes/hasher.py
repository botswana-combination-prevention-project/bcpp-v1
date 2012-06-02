import hashlib
from django.conf import settings


class Hasher(object):
    
    def get_hash(self, value):
        # only change algorithm if existing hashes have been updated
        hlib = hashlib.sha256()
        hlib.update(settings.SALT)
        hlib.update(value)
        return hlib