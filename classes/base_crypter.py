from bhp_string.classes import BaseString


class BaseCrypter(BaseString):

    # prefix for each segment of an encrypted value, also used to calculate
    # field length for model.
    HASH_PREFIX = 'enc1:::'  # uses a prefix to flag as encrypted
    SECRET_PREFIX = 'enc2:::'  # like django-extensions does
    IV_PREFIX = 'iv:::'

    def is_encrypted(self, value, prefix=None):
        """ The value string is considered encrypted if it starts
        with 'self.HASH_PREFIX' or whichever prefix is passed."""
        if prefix is None:
            prefix = self.HASH_PREFIX
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

    def mask(self, value, mask='<encrypted>'):
        """ Help format values for display by masking them if encrypted
        at the time of display."""
        if self.is_encrypted(value):
            return mask
        else:
            return value

    def make_random_salt(self, length=12, allowed_chars=('abcdefghijklmnopqrs'
                                                         'tuvwxyzABCDEFGHIJKL'
                                                         'MNOPQRSTUVWXYZ01234'
                                                         '56789!@#%^&*()?<>.,'
                                                         '[]{}')):
        return self.get_random_string(length, allowed_chars)
