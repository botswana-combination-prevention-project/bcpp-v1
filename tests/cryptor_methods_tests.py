from M2Crypto import Rand, RSA
from django.test import TestCase
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from bhp_crypto.classes import Cryptor, FieldCryptor
from bhp_crypto.fields import EncryptedFirstnameField, EncryptedLastnameField
from bhp_crypto.exceptions import AlgorithmError, EncryptionKeyError, ModeError


class CryptorMethodsTests(TestCase):

    """"""
    def test_base_cryptor_load_keys(self):
        # assert raises error when init with bogus algorithm
        self.assertRaises(AlgorithmError, Cryptor, 'nsa')
        self.assertRaises(ModeError, Cryptor, 'aes', 'irreversible')

        # init with just algorithm
        cryptor = Cryptor('rsa')
        # assert cannot set public/private key with just rsa algorithm
        self.assertRaises(EncryptionKeyError, cryptor.set_public_key)
        self.assertRaises(EncryptionKeyError, cryptor.set_private_key)
        cryptor = Cryptor('aes')
        # assert cannot set public/private key with just aes algorithm
        self.assertRaises(EncryptionKeyError, cryptor.set_public_key)
        self.assertRaises(EncryptionKeyError, cryptor.set_private_key)
        # init with algorithm and mode
        cryptor = Cryptor('rsa', 'restricted')
        # assert loads public key
        self.assertTrue(cryptor.set_public_key())
        # assert irreversible does not load private key
        self.assertTrue(cryptor.set_private_key())
        # init with algorithm and mode
        cryptor = Cryptor('rsa', 'local')
        self.assertTrue(cryptor.set_public_key())
        self.assertTrue(cryptor.set_private_key())
        # init with algorithm and mode
        cryptor = Cryptor('rsa', 'irreversible')
        # assert loads public key
        self.assertTrue(cryptor.set_public_key())
        # assert irreversible does not load private key
        self.assertFalse(cryptor.set_private_key())
        # init with algorithm and mode
        cryptor = Cryptor('aes', 'local')
        # assert aes does not load public key
        self.assertFalse(cryptor.set_public_key())
        # assert aes does not load private key
        self.assertFalse(cryptor.set_private_key())
        # assert aes loads aes key
        self.assertTrue(cryptor.set_aes_key())
        value = 'ABCDEF12345'
        #assert that an instance init with aes cannot call rsa_encrypt
        self.assertRaises(ImproperlyConfigured, cryptor.rsa_encrypt, value)
        cryptor = Cryptor('rsa', 'local')
        encrypted_value = cryptor.rsa_encrypt(value)
        self.assertEqual(value, cryptor.rsa_decrypt(encrypted_value, is_encoded=False))
        cryptor = Cryptor('rsa', 'irreversible')
        encrypted_value = cryptor.rsa_encrypt(value)
        # assert cannot decrypt irreversible
        self.assertEqual(encrypted_value, cryptor.rsa_decrypt(encrypted_value, is_encoded=False))
        cryptor = Cryptor('aes', 'local')
        encrypted_value = cryptor.aes_encrypt(value)
        self.assertEqual(value, cryptor.aes_decrypt(encrypted_value, is_encoded=True))

    def test_base_cryptor_mask(self):

        value = 'ABCDEF12345'
        cryptor = Cryptor('rsa', 'local')
        self.assertFalse(cryptor.is_encrypted(value))
        encrypted_value = cryptor.rsa_encrypt(value)
        re_encrypted_value = cryptor.rsa_encrypt(encrypted_value)

        print encrypted_value
        self.assertTrue(cryptor.is_encrypted(encrypted_value))
        self.assertEqual(cryptor.mask(encrypted_value), '<encrypted>')

    def test_field_cryptor(self):
        value = 'ABCDEF12345'
        field_cryptor = FieldCryptor('rsa', 'local')
        self.assertFalse(field_cryptor.is_encrypted(value))
        encrypted_value = field_cryptor.encrypt(value)
        self.assertEqual(value, field_cryptor.decrypt(encrypted_value))

        #re_encrypted_value = field_cryptor.rsa_encrypt(encrypted_value)
        self.assertTrue(field_cryptor.is_encrypted(encrypted_value))
        self.assertEqual(field_cryptor.cryptor.mask(encrypted_value), '<encrypted>')
