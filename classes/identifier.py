import re
from datetime import datetime
from django.db import IntegrityError
from bhp_identifier.models import IdentifierTracker
from bhp_identifier.exceptions import IdentifierError
from bhp_identifier.exceptions import CheckDigitError, IdentifierEncodingError, IdentifierDecodingError, IndentifierFormatError


class Identifier(object):

    """
    Create or increment identifier base36 encoded based on a given site_code
    and the year.

    Parts of Encode(), Decode() from http://en.wikipedia.org/wiki/Base_36
    """

    def __init__(self, **kwargs):
        self._counter_segment = None
        self._counter_length = None
        self._root_length = None
        self._root_segment = None
        self._pad_char = None
        self._modulus = None
        self._counter = None
        self._encoding = None
        self._identifier_tracker = None
        self._identifier = None
        self._identifier_string = None
        self._locked = False
        self._has_check_digit = False
        self._add_check_digit = True
        self._mm = kwargs.get('mm', str(datetime.now().strftime('%m')))
        self._yy = kwargs.get('yy', str(datetime.now().strftime('%y')))
        self.set_site_code(kwargs.get('site_code', '1'))
        self.protocol_code = kwargs.get('protocol_code', '')
        self.set_encoding(kwargs.get('encoding', 'base36'))
        self.set_counter_length(kwargs.get('counter_length', 1))
        self.set_identifier_type(kwargs.get('identifier_type', 'unknown'))

    def __unicode__(self):
        return self.get_identifier()

    def create(self, root_segment=None, counter_length=None, has_check_digit=None):
        """Create a new identifier."""
        if has_check_digit:
            # either it has a check digit or it will get one before encoding
            self._add_check_digit = False
        if counter_length:
            self.set_counter_length(counter_length)
        self.set_root_segment(root_segment)
        self._set_identifier()
        return self.get_identifier()

    def create_with_root(self, root_segment, counter_length=None):

        """Create a new system-wide unique identifier with a given root segment
        with or without a counter segment depending on the value of
        counter_length.
        """
        return self.create(root_segment, counter_length)

    def get_lock(self):
        return self._locked

    def lock(self):
        self._locked = True

    def unlock(self):
        self._locked = False

    def check_digit(self, number):
        """ Adds a check_digit to number. """
        if not isinstance(number, (int, long)):
            raise CheckDigitError('value used to calculate the check digit must be an integer.')
        return number % self.get_modulus()

    def increment(self):
        """Increments last counter by 1 using last counter (or None) from IdentifierTracker model
           for given root_segment and create a new IdentifierTracker record."""

        last_identifier = IdentifierTracker.objects.filter(root_number=self.get_root_segment()).order_by('-counter')
        if last_identifier:
            self.set_counter(last_identifier[0].counter + 1)
        else:
            self.set_counter(1)
        try:
            # create record, we'll update with the identifier later
            self._identifier_tracker = IdentifierTracker(
                root_number=self.get_root_segment(),
                counter=self.get_counter(),
                identifier_type=self.get_identifier_type(),
                )
            self._identifier_tracker.save()
        except IntegrityError as e:
            raise e
        except:
            raise IdentifierError('Failed to save() to IdentifierTracker table, your identifier was not created. Is it unique?')

    def update_tracker(self):
        """update our IdentifierTracker record with created identifier"""
        self._identifier_tracker.identifier = self.get_identifier()
        self._identifier_tracker.identifier_string = self._get_identifier_string()
        self._identifier_tracker.save()

    def set_site_code(self, value):
        if not re.match('\d+', value):
            raise IndentifierFormatError('Site code must be a string of numbers. Got {0}.'.format(value))
        self._site_code = value

    def get_site_code(self):
        return self._site_code

    def set_root_length(self, value):
        self._root_length = value

    def get_root_length(self):
        if not self._root_length:
            self.set_root_length()
        return self._root_length

    def set_given_root_segment(self, value):
        self._given_root_segment = value

    def get_given_root_segment(self):
        if not self._given_root_segment:
            self.set_given_root_segment(None)
        return self._given_root_segment

    def set_root_segment(self, value=None):
        """Derives the root segment of the identifier from either a given segment or site, protocol, date."""
        if value:
            self._root_segment = str(value)
        else:
            """Set root_segment, un-encoded root_segment, as site_code + protocol_code + 2digitmonth + 2digityear"""
            self._root_segment = "%s%s%s%s" % (self.get_site_code(), self.protocol_code, self._mm, self._yy.rjust(2, '0'))
        self.set_root_length(len(self._root_segment))

    def get_root_segment(self):
        if not self._root_segment:
            self.set_root_segment()
        return self._root_segment

    def get_counter_segment(self):
        if self.get_counter_length() == 0:
            # in this case, identifier string will have no counter segment
            return ''
        else:
            return  str(self.get_counter()).rjust(self.get_counter_length(), self.get_pad_char())

    def set_counter_length(self, value):
        if not isinstance(value, int):
            raise TypeError('Counter length must be an integer.')
        if not value > 0:
            raise IdentifierError('Identifier counter length must be greater than 0. Got {0}.'.format(value))
        self._counter_length = value

    def get_counter_length(self):
        if self._counter_length == None:
            raise IdentifierError('Counter length cannot be None. Set in __init__.')
        return self._counter_length

    def set_counter(self, value=None):
        if not value:
            value = 0
        self._counter = value

    def get_counter(self):
        if not self._counter:
            self.set_counter()
        return self._counter

    def set_modulus(self, value=None):
        if not value:
            value = 7
        if not isinstance(value, int):
            raise IdentifierError('Modulus must be an integer. Got {0}'.format(value))
        self._modulus = value

    def get_modulus(self):
        if not self._modulus:
            self.set_modulus()
        return self._modulus

    def set_pad_char(self, value=None):
        if not value:
            value = '0'
        self._pad_char = value

    def get_pad_char(self):
        if not self._pad_char:
            self.set_pad_char()
        return self._pad_char

    def set_encoding(self, value):
        self._encoding = value

    def get_encoding(self):
        if not self._encoding:
            raise IdentifierError('Encoding cannot be None.')
        return self._encoding

    def _set_identifier(self):
        #before encoding, increment counter for this root_segment and create an IdentifierTracker record
        self.increment()
        # set the identifier
        self._identifier = self.encode(int(self._get_identifier_string()), self.get_encoding(), has_check_digit=True)
        # update the tracker
        self.update_tracker()

    def get_identifier(self):
        if not self._identifier:
            raise IdentifierError('Attribute self._identifier cannot be None. Call set_identifier() first.')
        return self._identifier

    def _get_identifier_string(self):
        """Concat string of self._root_segment with padded string of counter, which must be able to convert to an INT"""
        string = "{0}{1}".format(self.get_root_segment(), self.get_counter_segment())
        if string[0] == '0':
            raise IndentifierFormatError('Identifier string cannot start with \'0\'. Got {0}'.format(string))
        check_digit = ''
        if self._add_check_digit:
            check_digit = self.check_digit(int(string))
        return "{0}{1}{2}".format(self.get_root_segment(), self.get_counter_segment(), check_digit)

    def set_identifier_type(self, value):
        self._identifier_type = value

    def get_identifier_type(self):
        return self._identifier_type

    def encode(self, unencoded_value, encoding, has_check_digit=True, alphabet='0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'):
        """Converts positive integer to a base36 string.
        Args:
            has_check_digit: if True, will confirm the check digit before encoding."""
        if not isinstance(unencoded_value, (int, long)):
            raise IdentifierEncodingError('unencoded_value passed for encoding must be an integer. Got {0}'.format(unencoded_value))
        if has_check_digit:
            unencoded_string = str(unencoded_value)
            if not int(unencoded_string[0:-1]) % self.get_modulus() == int(unencoded_string[-1]):
                raise CheckDigitError('Invalid unencoded_value. Has_check_digit=True so last digit should be %s which is the modulus %s of %s, Got %s' % (int(unencoded_string[0:-1]) % self.get_modulus(), self.get_modulus(), unencoded_string[0:-1], unencoded_string[-1]))
        if encoding:
            if encoding == 'base36':
                # Special case for zero
                if unencoded_value == 0:
                    encoded_value = alphabet[0]
                base36 = ''
                sign = ''
                if unencoded_value < 0:
                    sign = '-'
                    unencoded_value = -unencoded_value
                while unencoded_value != 0:
                    unencoded_value, i = divmod(unencoded_value, len(alphabet))
                    base36 = alphabet[i] + base36
                encoded_value = sign + base36
            else:
                raise IdentifierEncodingError('Invalid or unhandled encoding parameter. Got {0}'.format(encoding))
        if not encoded_value:
            raise IdentifierEncodingError('Value was not encoded.')
        return encoded_value

    def decode(self, encoded_value, encoding, has_check_digit=True):
        """Decodes an encoded value and confirms check digit if it has one."""
        if encoding == 'base36':
            decoded_number = str(int(encoded_value, 36))
        else:
            raise IdentifierDecodingError('Attribute encoding is invalid or unhandled. Got {0}'.format(encoding))
        if has_check_digit:
            # assume last digit is the check digit
            if not int(decoded_number[0:-1]) % self.get_modulus() == int(decoded_number[-1]):
                check_digit = int(decoded_number[0:-1]) % self.get_modulus()
                raise CheckDigitError('Invalid identifier after decoding. Last digit should be {0} which is the modulus {1} of {2}, Got {3}'.format(check_digit, self.get_modulus(), decoded_number[0:-1], decoded_number[-1]))
        return int(decoded_number)
