import re
from datetime import datetime
from bhp_common.models import IdentifierTracker

"""
from bhp_common.classes import Identifier
id=Identifier(identifier_type='receive', site_code='10')
x = id.create()
print x 
x.decode()
id.is_valid(x)

"""

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
            self.value=None
        else:    
            if re.match(self.re, str(value)):
                self.value = str(value)
            else:
                raise AttributeError, "Can't set attribute %s. %s. Got %s" % (self.name, self.msg, value)
    
class SiteCodeDescriptor(Descr):
    """Site_code descriptor."""
    def __init__(self):
        super(SiteCodeDescriptor, self).__init__()
        self.name = 'site_code'
        self.re = r'^[1-9]{1}[0-9]{1}$'
        self.msg = 'Must be 2 digit numeric not starting with \'0\'.'

class RootNumberDescriptor(Descr):
    """Root_number descriptor that must be int of given length."""
    def __init__(self, root_length=4):
        super(RootNumberDescriptor, self).__init__()    
        self.name = 'root_number'
        self.re = r'^[1-9]{1}[0-9]{%s}$' % (root_length - 1)
        self.msg = 'Must be %s digit numeric not starting with \'0\'.' % root_length

class CounterDescriptor(Descr):
    """Counter descriptor that must be int after padding."""
    def __init__(self, pad_length, pad_char):
        super(CounterDescriptor, self).__init__()
        self.name = 'counter'
        self.re = r'^[0-9]{1,%s}$' % pad_length
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
        self.re = r'^[A-Z0-9]{%s}' % length
        self.msg = 'Must be an alphanumeric in uppercase of character length %s. Check counter padding or root length before encoding.'  % length

class Identifier(object):

    """
    Create or increment identifier base36 encoded based on a given site_code and the year.
    
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
        
        Encode, decode parts from http://en.wikipedia.org/wiki/Base_36
    """

    # padding length for counter segment of un-encoded identifier
    pad_length = 6
    # counter padding character
    pad_char = '0'
    # root_length before encoding cannot be less that 4 (sitecode+yy)
    root_length = 4
    # identifier_length after encodeing
    identifier_length = 7        
    # descriptors
    site_code = SiteCodeDescriptor()
    root_number =RootNumberDescriptor(root_length)        
    counter = CounterDescriptor(pad_length, pad_char)
    identifier_string = IdentifierStringDescriptor()
    identifier = IdentifierDescriptor(identifier_length)
    
    def __init__(self, **kwargs):
        self.created = False 
        self.locked=False              
        self.modulus = 10
        self.site_code = kwargs.get('site_code','')
        self.identifier_type = kwargs.get('identifier_type', 'unknown')
        self.identifier_tracker = None

    
    def __unicode__(self):
        return self.identifier
            
    def create(self):
        """Create a new identifier based on the given site_code"""       
          
        #before encoding, increment counter for this root_number and create an IdentifierTracker record
        self.increment()        

        # put together a string for encoding
        self.set_identifier_string()
        
        # add an extra digit as a check digit to the end of the identifier string
        self.add_check_digit()
        
        # encode the string
        self.identifier = self.encode(int(self.identifier_string))
        
        # update the IdentifierTracker record created when you incremented the counter
        self.update_tracker()

        # flag as created (in case you call next())
        self.created = True            

        return self.identifier

    def lock(self):
        self.locked=True

    def unlock(self):
        self.locked=False    
    
    def add_check_digit(self):
        check_digit = int(self.identifier_string) % self.modulus
        self.identifier_string = '%s%s' % ( self.identifier_string, check_digit)
    
    def is_valid(self, identifier):
        """Returns True if modulus 10 of decoded identifier (less  last digit) equals the check_digit (last digit)."""
        x = self.decode(identifier)
        check_digit = int(str(x)[-1])
        x = int(str(x)[0:-1])
        return x % self.modulus == check_digit
        
    
    def increment(self):

        """Increment last counter by 1 using last counter (or None) from IdentifierTracker model for given root_number and create a new IdentifierTracker record."""
        
        self.set_root_number()        
        self.lock()
        last_identifier = IdentifierTracker.objects.filter(root_number=self.root_number).order_by('-counter')
        if last_identifier:
            self.counter = last_identifier[0].counter + 1
            self.unlock()            
        else:
            self.counter = 1

        try:
            # create record, we'll update with the identifier later
            self.identifier_tracker = IdentifierTracker(
                root_number = self.root_number,
                counter = self.counter,
                identifier_type = self.identifier_type,
                )
            self.identifier_tracker.save()    
            self.created = True            
            self.unlock()
        except:
            self.unlock()        
            counter = None
            raise 'Failed to save() IdentifierTracker, identifier not created'
    
    def update_tracker(self):
        """update our IdentifierTracker record with created identifier"""
        self.identifier_tracker.identifier = self.identifier
        self.identifier_tracker.save()
    
    def set_root_number(self):
        """Set root_number, un-encoded root_segment, as site_code + year"""
        self.root_number = "%s%s" % (self.site_code, str(datetime.now().strftime('%y')).rjust(self.root_length-len(self.site_code),'0'))
        
    def set_identifier_string(self):
        """Concat string of root_number with padded string of counter, which must convert to an INT"""
        self.identifier_string = "%s%s" % (self.root_number, self.counter.rjust(self.pad_length, self.pad_char))

    def encode(self, number, alphabet='0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'):
   
        """Convert positive integer to a base36 string."""
        
        if not isinstance(number, (int, long)):
            raise TypeError('number must be an integer')
     
        # Special case for zero
        if number == 0:
            return alphabet[0]
     
        base36 = ''
     
        sign = ''
        if number < 0:
            sign = '-'
            number = - number
     
        while number != 0:
            number, i = divmod(number, len(alphabet))
            base36 = alphabet[i] + base36
     
        return sign + base36
        
    def decode(self, number):
        return int(number, 36)
