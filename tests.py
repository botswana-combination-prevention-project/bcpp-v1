from datetime import datetime
from django.utils import unittest
from bhp_identifier.classes import Identifier
from bhp_identifier.models import IdentifierTracker
from bhp_identifier.exceptions import CheckDigitError

"""
from django.utils import unittest
from bhp_common.tests import IdentifierTestCase
suite = unittest.TestLoader().loadTestsFromTestCase(IdentifierTestCase)
unittest.TextTestRunner(verbosity=2).run(suite)
"""

class IdentifierTestCase(unittest.TestCase):

    """In addition to create() and create_with_root(), test encodeing/decoding with and without check digits for passed encoded_numbers/decoded_numbers."""

    def setUp(self):

        self.id = None
        if IdentifierTracker.objects.filter(identifier_string = '123123123'):
            IdentifierTracker.objects.get(identifier_string = '123123123').delete()
        
    def testEncode(self):

        if IdentifierTracker.objects.filter(identifier_string = '123123123'):
            IdentifierTracker.objects.get(identifier_string = '123123123').delete()
        self.id = Identifier(identifier_type = 'subject')    
        
        #check default for encode
        self.assertEqual(self.id.encode(123123123), 'KD1K3M')                  
        self.assertEqual(self.id.identifier_string, '123123123')
        self.assertEqual(self.id.identifier, 'KD1K3M')              
        self.assertEqual(self.id.is_valid(), True)        
        
        # specify has_check_digit = False
        self.assertEqual(self.id.encode(123123123, False), 'KD1K3M')
        self.assertEqual(self.id.identifier_string, '123123123')
        self.assertEqual(self.id.identifier, 'KD1K3M')              
        self.assertEqual(self.id.is_valid(), True)      
                  
        # specify has_check_digit = True
        self.assertRaises(CheckDigitError, self.id.encode(1231231234, True))
        self.assertEqual(self.id.identifier_string, '123123123')
        self.assertEqual(self.id.identifier, 'KD1K3M')              
        self.assertEqual(self.id.is_valid(), True)        

        # specify has_check_digit = True, but check_digit is invalid
        try:
            self.id.encode(1231231235, True)
        except:
            error_occured = True
        self.assertTrue(error_occured)

    def testDecode(self):

        if IdentifierTracker.objects.filter(identifier_string = '123123123'):
            IdentifierTracker.objects.get(identifier_string = '123123123').delete()
        self.id = Identifier(identifier_type = 'subject')
        self.assertEqual(self.id.decode('21AYER'),  '123123123')
        self.assertEqual(self.id.identifier_string, '123123123')
        self.assertEqual(self.id.identifier, '21AYER')                        
        self.assertEqual(self.id.is_valid(), False)    

        # specify has_check_digit = True, but check_digit is invalid in encoded number
        try:
            self.id.decode('KD1K3', True)
        except:
            error_occured = True
        self.assertTrue(error_occured)
        
    def testCreate(self):

        self.id = Identifier(identifier_type = 'subject', site_code = '10', protocol_code = '041', counter_length = 6)    
        self.id.create()
        self.assertEqual(self.id.counter_segment, '%s' % str(self.id.counter).rjust(6,'0'))
        self.assertEqual(self.id.root_segment, '10041%s%s' % (str(datetime.now().strftime('%m')), str(datetime.now().strftime('%y')).rjust(2,'0')))        
        self.assertEqual(self.id.identifier_string , '10041%s%s%s' % (str(datetime.now().strftime('%m')), str(datetime.now().strftime('%y')).rjust(2,'0'),str(self.id.counter).rjust(6,'0')))        
        self.assertEqual(self.id.is_valid(), True)        

    def testCreateWithRoot(self):

        if IdentifierTracker.objects.filter(identifier_string = '123123123'):
            IdentifierTracker.objects.get(identifier_string = '123123123').delete()
        self.id = Identifier(identifier_type = 'subject')        
        self.id.create_with_root('123123123')
        self.assertEqual(self.id.identifier_string, '123123123')
        self.assertEqual(self.id.identifier, 'KD1K3M')                        
        
        self.id.create_with_root('123123123', 10)        
        self.assertEqual(self.id.identifier_string, '123123123%s' % str(self.id.counter).rjust(10,'0'))
        #self.assertEqual(self.id.identifier, '2LJJYG9WOWE8Z')                        
        self.assertEqual(int(self.id.identifier, 36), int('%s%s' % (self.id.identifier_string, int(self.id.identifier_string) % self.id.modulus)))
        self.assertEqual(self.id.is_valid(), True)
        
