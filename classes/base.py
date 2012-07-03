from bhp_string.classes import BaseString

class Base(BaseString):
    
    def make_random_salt(self, length=12, allowed_chars='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#%^&*()?<>.,[]{}'):
        
        return self.get_random_string(length, allowed_chars)
    

        