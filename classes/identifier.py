import re
from datetime import datetime
from bhp_common.models import IdentifierTracker

"""
from bhp_common.classes import Identifier
id=Identifier()
id.create(site_code='10')
"""

class Identifier(object):

    """
    Encode, decode parts from http://en.wikipedia.org/wiki/Base_36
    """

    def __init__(self):
        
        self.created = False   
        self.identifier = ''
        self.site_code='00'     
       
    def create(self, **kwargs):
       
        # site_numeric is a required parameter
        self.site_code = kwargs.get('site_code', self.site_code)
        if re.match(r'[1-9]{1}[0-9]{1}', self.site_code):
            self.site_code = str(self.site_code)        
        else:            
            raise TypeError("Identifier requires a 2 digit numeric site_code that cannot start with \'0\'. Got %s" % self.site_code)

        self.identifier = kwargs.get('identifier', self.identifier)
        
        if self.identifier:
            if not re.match(r'[A-Z0-9]{7}', self.identifier):            
                raise TypeError("Identifier requires a 7 digit alphanumeric root_number. Got %s" % self.identifier)
    
        
        #before encoding, determine root_number and counter
        root_number = self.get_root_number(self.identifier)
    
        # need to lock now as the counter comes from the db table
        self.lock()

        counter = self.lookup_next_counter(root_number)        
        
        identifier_string = self.format(root_number, counter)
        #raise TypeError(identifier_string)
        
        self.identifier = self.encode(int(identifier_string))

        try:
            IdentifierTracker.objects.create(
                identifier = self.identifier,
                root_number = root_number,
                counter = counter,
                )
            self.created = True            
            self.unlock()
        except:
            self.unlock()        
            raise 'Failed to update IdentifierTracker, identifier not created'
            
        return self.identifier

    def lock(self):
        pass

    def unlock(self):
        pass        
    
    def lookup_next_counter(self,root_number):
    
        last_identifier = IdentifierTracker.objects.filter(root_number=root_number).order_by('-counter')

        if last_identifier:
            counter = last_identifier[0].counter + 1
            if counter > 999999:
                raise TypeError("Identifier cannot create more than 999,999 identifiers per year")
        else:
            counter = 1
    
        return counter
    
    def get_root_number(self, root_number):
    
        if self.identifier:
            root_number = str(self.decode(self.identifier))[0:4]
        else:    
            root_number = self.site_code + str(datetime.now().strftime('%y')).rjust(2,'0')
        
        return root_number

    def format(self, root_number, counter, pad_length=7, pad_string='0'):
        string = str(root_number) + str(counter).rjust(pad_length, pad_string)
        try:
            int(string)
        except:
            raise TypeError('Identifier could not convert decoded identifier string to int')  
        return str(root_number) + str(counter).rjust(pad_length, pad_string)

    def next(self):
        
        if self.created:
            self.created = False
            next_id = self.create()    
            
        return next_id    
        
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
