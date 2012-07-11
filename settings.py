#from django.conf import settings as django_settings
#
#
#class Settings( object ):
#    
#    def __init__(self):
#        self._register = {}        
#        self._register.update(django_settings.BHP_CRYPTO_SETTINGS)
#            
#    @property
#    def SALT(self):
#        return self._register.get('SALT', '')
#    
#    @property
#    def IS_SECURE_DEVICE(self):
#        return self._register.get('IS_SECURE_DEVICE', False)
#
#    @property
#    def PUBLIC_KEY_RESTRICTED(self):
#        return self._register.get('PUBLIC_KEY_RESTRICTED', '')
#
#    @property
#    def PRIVATE_KEY_RESTRICTED(self):
#        return self._register.get('PRIVATE_KEY_RESTRICTED', '')
#
#    @property
#    def PUBLIC_KEY_LOCAL(self):
#        return self._register.get('PUBLIC_KEY_LOCAL', '')
#
#    @property
#    def PRIVATE_KEY_LOCAL(self):
#        return self._register.get('PRIVATE_KEY_LOCAL', '')
#
#    @property
#    def AES_KEY(self):
#        return self._register.get('AES_KEY', '')
#
#    @property
#    def MAY_CREATE_NEW_KEYS(self):
#        return self._register.get('MAY_CREATE_NEW_KEYS', False)
#
#settings = Settings()
