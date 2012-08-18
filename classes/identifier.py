import re
from datetime import datetime
from bhp_identifier.models import IdentifierTracker


class Descr(object):
    """Base descriptor, converts value to string on set."""
    def __init__(self):
        self.name = ''
        self.re = r''
        self.msg = ''
        self.value = None
        self.error = ''

    def __get__(self, instance, owner):
        return self.value

    def __set__(self, instance, value):
        if not value:
            self.value = ''
        else:
            if re.match(self.re, str(value)):
                self.value = str(value)
            else:
                raise AttributeError("Can't set attribute {0}. {1}. Got {2}"
                                     .format(self.name, self.msg, value))


class SiteCodeDescriptor(Descr):
    """Site_code descriptor."""
    def __init__(self):
        super(SiteCodeDescriptor, self).__init__()
        self.name = 'site_code'
        self.re = r'^[1-9]{1}[0-9]{1}$'
        self.msg = 'Must be 2 digit numeric not starting with \'0\'.'


class ProtocolCodeDescriptor(Descr):
    """protocol_code descriptor."""
    def __init__(self):
        super(ProtocolCodeDescriptor, self).__init__()
        self.name = 'protocol_code'
        self.re = r'^[0-9]{3}$'
        self.msg = 'Must be 3 digit numeric.'


class RootSegmentDescriptor(Descr):
    """self.root_segment descriptor that must be int of given length."""
    def __init__(self, root_length):
        super(RootSegmentDescriptor, self).__init__()
        self.name = 'root_segment'
        self.re = r'^[1-9]{1}[0-9]{%s}$' % (root_length - 1)
        self.msg = 'Must be %s digit numeric not starting with \'0\'.' % root_length

    def update_attr(self, root_length):
        self.re = r'^[1-9]{1}[0-9]{%s}$' % (root_length - 1)
        self.msg = 'Must be %s digit numeric not starting with \'0\'.' % root_length


class CounterSegmentDescriptor(Descr):
    """Counter descriptor that must be int after padding."""
    def __init__(self, pad_length, pad_char):
        super(CounterSegmentDescriptor, self).__init__()
        self.name = 'counter'
        self.re = r'^[0-9]{%s}$' % pad_length
        self.msg = 'Must be 1-%s digit numeric.' % pad_length


class IdentifierStringDescriptor(Descr):
    """Identifier string descriptor that will be converted to an int later."""
    def __init__(self):
        super(IdentifierStringDescriptor, self).__init__()
        self.name = 'identifier_string'
        self.re = r'^\d+'
        self.msg = 'Must be a string that can be converted to an integer using int().'


class IdentifierDescriptor(Descr):
    """Identifier descriptor that must be alphanumeric of given length."""
    def __init__(self, length=7):
        super(IdentifierDescriptor, self).__init__()
        self.name = 'identifier'
        self.re = r'^[A-Z0-9]{1,%s}' % length
        self.msg = 'Must be an alphanumeric in uppercase of character length %s. Check counter padding or root length before encoding.' % length


class Identifier(object):

    """
    Create or increment identifier base36 encoded based on a given site_code
    and the year.

        Note that the check-digit is part of the encoded number but not the
        decoded_number

        If a decoded number is passed without a check digit, it will be added
        before encoding but remove after decoding.

        If a number is passed to the encoder with a check_digit, it will be
        remove upon decoding.

        So self.identifier_string does NOT contain the check digit.

        see unittest in tests.py

        Example:
        >>> site_code = '10'
        >>> id = Identifier(identifier_type='requisition', site_code='10')
        >>> id.create()
        '4N78DXT'
        >>> id.create()
        '4N78DXU'
        >>> id.site_code = '44'
        >>> id.create()
        'K9HYDTX'
        >>> Identifier().decode('K9HYDTX')
        44110000005L
        >>> id.is_valid(x)
        True

        parts of Encode(), Decode() from http://en.wikipedia.org/wiki/Base_36
    """

    # counter padding character
    pad_char = '0'

    # identifier_length after encodeing (does this do anything??)
    identifier_length = 7

    # descriptors
    site_code = SiteCodeDescriptor()
    protocol_code = ProtocolCodeDescriptor()
    identifier_string = IdentifierStringDescriptor()
    identifier = IdentifierDescriptor(identifier_length)

    def __init__(self, **kwargs):

        self.created = False
        self.locked = False
        self.modulus = 7
        self.has_check_digit = False
        self.counter = 0
        self.site_code = kwargs.get('site_code', '')
        self.protocol_code = kwargs.get('protocol_code', '')
        self.given_root_segment = kwargs.get('root_segment', '')
        # padding length for counter segment of un-encoded identifier
        # this will affect total number of unique identifiers for the
        # current root_segement, e.g. 4 => 0-9999. (If root_segement
        # has site, protocol and year)
        # if counter_length == 0, will not add a counter_segment
        self.counter_length = kwargs.get('counter_length', 5)
        self.counter_segment = CounterSegmentDescriptor(self.counter_length, self.pad_char)
        self.identifier_type = kwargs.get('identifier_type', 'unknown')
        self.identifier_tracker = None
        self.identifier = None
        self.identifier_string = None

    def __unicode__(self):
        return self.identifier

    def create(self):
        """Create a new identifier based on the given site_code"""
        # root segement length is site_code + protocol_code + 4 (MMYY)
        self.root_length = len(self.site_code) + len(self.protocol_code) + 4
        self.root_segment = RootSegmentDescriptor(self.root_length)
        self.set_root_segment()
        #before encoding, increment counter for this root_segment and create an IdentifierTracker record
        self.increment()
        # put together a string for encoding
        self.set_identifier_string()
        # encode the string
        self.encode()
        # update the IdentifierTracker record created when you incremented the counter
        self.update_tracker()
        # flag as created (in case you call next())
        self.created = True
        return self.identifier

    def create_with_root(self, given_root_segment, counter_length=0):

        """Create a new system-wide unique identifier with a given root segment
        with or without a counter segment depending on the value of
        counter_length.
        """
        given_root_segment = str(given_root_segment)
        self.counter_length = counter_length
        self.root_length = len(given_root_segment)
        self.root_segment = RootSegmentDescriptor(self.root_length)
        self.root_segment = given_root_segment
        #before encoding, increment counter for this root_segment and create an
        #IdentifierTracker record
        self.increment()
        # put together a string for encoding
        self.set_identifier_string()
        # encode the string
        self.encode()
        # update the IdentifierTracker record created when you incremented
        # the counter
        self.update_tracker()
        # flag as created (in case you call next())
        self.created = True
        return self.identifier

    def lock(self):
        self.locked = True

    def unlock(self):
        self.locked = False

    def check_digit(self, number=None):

        """ add check_digit using the final identifier_string """
        if not number:
            number = int(self.identifier_string)
        return number % self.modulus

    def is_valid(self, identifier=None, encoded=True):
        """Returns True if modulus of encoded/decoded identifier
        (less last digit) equals the check_digit (last digit).
        """
        if not identifier:
            identifier = self.identifier
        if encoded:
            x = self.decode(identifier)
        else:
            if not isinstance(identifier, (int, long)):
                raise TypeError('Identifier must be an integer if encode=False')
            x = identifier

        check_digit = int(str(x)[-1])
        x = int(str(x)[0:-1])
        return x % self.modulus == check_digit

    def increment(self):

        """Increment last counter by 1 using last counter (or None) from IdentifierTracker model 
           for given root_segment and create a new IdentifierTracker record."""
        if self.counter_length == 0:
            self.counter = 0
        else:
            self.lock()
            last_identifier = IdentifierTracker.objects.filter(root_number=self.root_segment).order_by('-counter')
            if last_identifier:
                self.counter = last_identifier[0].counter + 1
                self.unlock()
            else:
                self.counter = 1
        try:
            # create record, we'll update with the identifier later
            self.identifier_tracker = IdentifierTracker(
                root_number=self.root_segment,
                counter=self.counter,
                identifier_type=self.identifier_type,
                )
            self.identifier_tracker.save()
            self.created = True
            self.unlock()
        except:
            self.unlock()
            self.counter = 0
            raise TypeError('Failed to save() to IdentifierTracker table, your identifier was not created. Is it unique?')
        self.set_counter_segment()

    def update_tracker(self):
        """update our IdentifierTracker record with created identifier"""
        self.identifier_tracker.identifier = self.identifier
        self.identifier_tracker.identifier_string = self.identifier_string
        self.identifier_tracker.save()

    def set_root_segment(self):
        if self.given_root_segment:
            self.root_segment = self.given_root_segment
        else:
            """Set root_segment, un-encoded root_segment, as site_code + protocol_code + 2digitmonth + 2digityear"""
            self.root_segment = "%s%s%s%s" % (self.site_code, self.protocol_code, str(datetime.now().strftime('%m')), str(datetime.now().strftime('%y')).rjust(2, '0'))

    def set_counter_segment(self):
        if self.counter_length == 0:
            # in this case, identifier string will have no counter segment
            self.counter_segment = ''
        else:
            self.counter_segment = str(self.counter).rjust(self.counter_length, self.pad_char)

    def set_identifier_string(self):
        """Concat string of self.root_segment with padded string of counter, which must be able to convert to an INT"""
        self.identifier_string = "%s%s" % (self.root_segment, self.counter_segment)

    def encode(self, number=None, has_check_digit=False, alphabet='0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'):

        #coder = Coder()
        #coder.encode(number, has_check_digit, alphabet )
        """Convert positive integer to a base36 string."""
        # access internally as encode()
        # access and pass a number to encode, check_digit not part of the number
        # access and pass a number to encode, which includes a check_digit
        # always add check_digit (or add it back) before encoding
        if number:
            self.identifier_string = number
            # is last digit a check digit?
            if has_check_digit:
                # ok, but is it valid
                if self.is_valid(number, False):
                    # yes,
                    self.identifier_string = self.identifier_string[0:-1]
                else:
                    # no
                    raise ValueError('Invalid identifier. Last digit should be %s which is the modulus %s of %s, Got %s' % (int(str(number)[0:-1]) % self.modulus, self.modulus, str(number)[0:-1], str(number)[-1]))
        # we don't store the check_digit as part of the identifier_string, so add it back
        number = int(self.identifier_string + str(self.check_digit()))
        if not isinstance(number, (int, long)):
            raise TypeError('number must be an integer')
        # Special case for zero
        if number == 0:
            return alphabet[0]
        base36 = ''
        sign = ''
        if number < 0:
            sign = '-'
            number = -number
        while number != 0:
            number, i = divmod(number, len(alphabet))
            base36 = alphabet[i] + base36
        self.identifier = sign + base36
        return self.identifier

    def decode(self, base36=None, has_check_digit=False):

        if base36:
            self.has_check_digit = has_check_digit
            self.identifier = base36
        decoded_number = str(int(self.identifier, 36))
        if self.has_check_digit:
            # assume last digit is the check digit
            if int(decoded_number[0:-1]) % self.modulus == int(decoded_number[-1]):
                self.identifier_string = decoded_number[0:-1]
            else:
                raise ValueError(
                                 'Invalid identifier. Last digit should be {0} which is the modulus {1} of {2}, Got {3}'.format(decoded_number[0:-1] % self.modulus, self.modulus, decoded_number[0:-1], decoded_number[-1]))
        else:
            self.identifier_string = decoded_number
        return self.identifier_string
