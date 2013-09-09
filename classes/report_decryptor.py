from bhp_crypto.classes import Cryptor
from bhp_crypto.models import Crypt

class ReportDecryptor(Cryptor):
    
    def __init__(self):
        self.algorithm = 'rsa'
        self.mode = 'local'
        
    def decrypt(self, line, **kwargs):
        line = line.replace('<div>enc1:::','')
        line = line.replace('</div>','')
        line = line.strip()
        secret = Crypt.objects.filter(hash=line)
        #decrypted = Cryptor('rsa',mode='local').rsa_decrypt(secret)
        decrypted = self.rsa_decrypt(secret[0].secret)
        #print decrypted
        return '<div>'+decrypted+'</div>'