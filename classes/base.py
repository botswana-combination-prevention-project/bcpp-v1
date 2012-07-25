from bhp_string.classes import BaseString


class Base(BaseString):

    def __init__(self, *args, **kwargs):
        super(Base, self).__init__(*args, **kwargs)

    def make_random_salt(self, length=12, allowed_chars=('abcdefghijklmnopqrs'
                                                         'tuvwxyzABCDEFGHIJKL'
                                                         'MNOPQRSTUVWXYZ01234'
                                                         '56789!@#%^&*()?<>.,'
                                                         '[]{}')):
        return self.get_random_string(length, allowed_chars)
