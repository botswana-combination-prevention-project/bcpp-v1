from M2Crypto import Rand, RSA
from django.utils import unittest
from django.conf import settings
from classes import Crypter
from bhp_crypto.fields import StrongEncryptionField, WeakEncryptionField

"""
from django.utils import unittest
from bhp_crypto.tests import EncryptedFieldCase
suite = unittest.TestLoader().loadTestsFromTestCase(EncryptedFieldCase)
unittest.TextTestRunner(verbosity=2).run(suite)
"""

class CrypterTestCase(unittest.TestCase):

    """"""

    def setUp(self):
        self.value = 'ABCDEF12345'
        crypter = Crypter()
        crypter.public_key = settings.PUBLIC_KEY_STRONG
        crypter.private_key = settings.PRIVATE_KEY_STRONG
        
    def testEncrypt(self):

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
        
        #self.weak_field.public_key = settings.PUBLIC_KEY_WEAK
        #self.weak_field.private_key = settings.PRIVATE_KEY_WEAK
    
        field_strong_encrypted_value = crypter.encrypt(self.value, True)
        x = crypter.decrypt(field_strong_encrypted_value)
        #        print field_strong_encrypted_value
        #self.assertEqual(self.strong_field.crypter.decrypt(field_strong_encrypted_value), self.value)
        #self.assertEqual(self.strong_field.crypter.decrypt(strong_encrypted_value), self.value)
        
        
                

        