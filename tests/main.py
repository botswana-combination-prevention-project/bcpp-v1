from M2Crypto import Rand, RSA
from django.test import TestCase
from django.conf import settings
from bhp_crypto.classes import Cryptor
from bhp_crypto.fields import StrongEncryptionField, WeakEncryptionField

"""
from django.utils import unittest
from bhp_crypto.tests import EncryptedFieldCase
suite = unittest.TestLoader().loadTestsFromTestCase(EncryptedFieldCase)
unittest.TextTestRunner(verbosity=2).run(suite)
"""

class cryptor_methods_tests(TestCase):

    """"""

    def setup(self):
        self.value = 'ABCDEF12345'
        cryptor = Cryptor()

    def test_encrypt(self):
        encrypted_value = self.crypter.encrypt(self.value)
        decrypted_value = self.crypter.decrypt(encrypted_value)
        self.assertEqual(self.value, decrypted_value)

class EncryptedFieldCase(unittest.TestCase):
    
    def setUp(self):
        
        self.value = 'ABCDEF12345'
        self.strong_field = StrongEncryptionField()
        self.weak_field = WeakEncryptionField()
        
    def testStrongEncryption(self):

        crypter = Crypter()
        crypter.writer = RSA.load_pub_key(settings.PUBLIC_KEY_STRONG)
        strong_encrypted_value = crypter.writer.public_encrypt(self.value, RSA.pkcs1_oaep_padding)
        
        crypter.public_key = settings.PUBLIC_KEY_STRONG
        crypter.private_key = settings.PRIVATE_KEY_STRONG
        
        self.weak_field.public_key = settings.PUBLIC_KEY_WEAK
        self.weak_field.private_key = settings.PRIVATE_KEY_WEAK
    
        x = crypter.encrypt(self.value, True)
        y = crypter.decrypt(x)
        self.assertEqual(self.value,y)
        crypter.private_key = None
        y = crypter.decrypt(x)
        self.assertNotEqual(self.value,y)
        
        #        print field_strong_encrypted_value
        #self.assertEqual(self.strong_field.crypter.decrypt(field_strong_encrypted_value), self.value)
        #self.assertEqual(self.strong_field.crypter.decrypt(strong_encrypted_value), self.value)
        
        
                

        