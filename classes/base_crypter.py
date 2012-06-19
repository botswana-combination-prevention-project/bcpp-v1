import os, base64
from datetime import datetime
from M2Crypto import Rand, RSA, EVP

class BaseCrypter(object):
    
    KEY_LENGTH = 2048
    ENC=1
    DEC=0
    
    def set_public_key(self, keyfile):
        """ load public key """
        if keyfile:
            self.public_key = RSA.load_pub_key(keyfile)
        
    def set_private_key(self, keyfile):
        """ load the private key """
        if keyfile:
            self.private_key = RSA.load_key(keyfile)

    def set_aes_key(self, key):
        """ load the aes key """
        self.key = key
    
    def _blank_callback(self): 
        "Replace the default dashes as output upon key generation" 
        return
    
    
    def create_new_key_pair(self):
        """ create a new key-pair in the default folder, filename includes the current timestamp """        
        # have a suffix to the file names to prevent overwriting
        name = str(datetime.today())
        # Random seed 
        Rand.rand_seed (os.urandom (self.KEY_LENGTH)) 
        # Generate key pair 
        key = RSA.gen_key (self.KEY_LENGTH, 65537, self._blank_callback) 
        # Non encrypted key 
        key.save_key('user-private.pem.%s' % name, None) 
        # Use a pass phrase to encrypt key 
        #key.save_key('user-private.pem') 
        key.save_pub_key('user-public.pem.%s' % name)         
    
    def create_aes_key(self, key, public_keyfile):
        """ create and encrypt a new AES key. Use the "local" public key """
        self.set_public_key(public_keyfile)
        name = 'user-aes-local.pem.{0}'.format(str(datetime.today()))
        encrypted_key = self.public_key.public_encrypt(key, RSA.pkcs1_oaep_padding)   
        f = open(name, 'w') 
        f.write(base64.b64encode(encrypted_key))
        f.close()
        return base64.b64encode(encrypted_key)
    
    def rsa_encrypt(self, value):
        return self.public_key.public_encrypt(value, RSA.pkcs1_oaep_padding)

    def rsa_decrypt(self, cipher_text):
        cipher_text = cipher_text
        return self.private_key.private_decrypt(base64.b64decode(cipher_text),
                                                    RSA.pkcs1_oaep_padding).replace('\x00', '')

    def _build_cipher(self, key, iv=None, op=ENC):
        """"""""
        if iv is None:
                iv = '\0' * 16
        else:
            iv = base64.b64decode(iv)
        return EVP.Cipher(alg='aes_128_cbc', key=key, iv=iv, op=op)
                                                    
    def aes_decrypt(self, cipher_text):
        cipher_text = base64.b64decode(cipher_text)
        cipher = self._build_cipher(self.key, None, self.DEC)
        v = cipher.update(cipher_text)
        v = v + cipher.final()
        del cipher
        return v.replace('\x00', '')
    
    def aes_encrypt(self, value):            
        cipher = self._build_cipher(self.key, None, self.ENC)
        v = cipher.update(value)
        v = v + cipher.final()
        del cipher
        return v
   
    