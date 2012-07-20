__authors__ = [
    '"Erik van Widenfelt" <ew2789@gmail.com>',
]

import os

from bhp_string.classes import BaseString


class Base(BaseString):

    def __init__(self, *args, **kwargs):
        super(Base, self).__init__(*args, **kwargs)

    def all_keys_exist(self):

        pem = {'restricted_public': 'user-public-restricted.pem',
               'restricted_private': 'user-private-restricted.pem',
               'local_public': 'user-public-local.pem',
               'local_private': 'user-private-local.pem',
               'local-aes': 'user-aes-local', }

        #check for the existence of each key file
        for filename in pem.itervalues():
            if not os.path.exists(os.path.join('.', filename)):
                print '{0} not found.'.format(filename)

    def make_random_salt(self, length=12, allowed_chars=('abcdefghijklmnopqrs'
                                                         'tuvwxyzABCDEFGHIJKL'
                                                         'MNOPQRSTUVWXYZ01234'
                                                         '56789!@#%^&*()?<>.,'
                                                         '[]{}')):
        return self.get_random_string(length, allowed_chars)
