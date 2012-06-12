from django.db import models
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from crypter import Crypter


class BaseEncryptedField(models.Field):
    
    """ A field class that stores sensitive data in an encrypted format.
    
    To maintain uniqueness and searchability, only the hash is ever stored in the model field.
    
    If a cipher is generated, it is stored with the hash in the Crypt lookup model and will be
    made available when required for decryption (e.g. the private key is available)
       
    Hash salt, public key and private key are referred to via the settings file
    
    """

    __metaclass__ = models.SubfieldBase
    encryption_method = None
    valid_encryption_methods = ['strong', 'weak', 'hash-only']
    crypter = Crypter()
    
    def __init__(self, *args, **kwargs):  
        """
        The required field attribute 'encryption_method' guides in loading public and private keys
        
        1. strong: use on values that should be less convenient to decrypt. Private key is not
           allowed on mobile devices (settings.IS_MOBILE_DEVICE).
        2. weak: same as strong but the private key is expected to be available and is not checked for
        3. hash: irreversibly hash the value. do not create a corresponding cipher 
        """
        
        defaults = {}
        self.encryption_method = kwargs.get('encryption_method', 'public-key')
        if 'encryption_method' in kwargs:
            del kwargs['encryption_method']
        
        if self.encryption_method not in self.valid_encryption_methods:
            raise ImproperlyConfigured('Available options for EncryptedField field parameter' \
                                        '\'encryption_method\' are \'%s\'. Got \'%s\' ' \
                                        % ('\' or \''.join(self.valid_encryption_methods), kwargs.get('encryption_method')))
           
        if self.encryption_method == 'strong':
            defaults = {'help_text': kwargs.get('help_text', '') + ' (Encryption: strong)'}
            # load public key, private key (if available) and set writer
            if not hasattr(settings, 'IS_MOBILE_DEVICE'):
                raise ImproperlyConfigured('You must set the IS_MOBILE_DEVICE setting to True ' \
                                           'or False for \'strong\' encryption' )
            if not hasattr(settings, 'PUBLIC_KEY_STRONG'):
                raise ImproperlyConfigured('You must set the PUBLIC_KEY_STRONG setting to ' \
                                           'point to your public key (path and filename) .')
            self.crypter.public_key = settings.PUBLIC_KEY_STRONG
            if 'PRIVATE_KEY_STRONG' in dir(settings):
                # strong security DOES NOT expect a private key to be available on the device
                if settings.PRIVATE_KEY_STRONG:
                    if not settings.IS_MOBILE_DEVICE:
                        self.crypter.private_key = settings.PRIVATE_KEY_STRONG
                    else:
                        raise ImproperlyConfigured('PRIVATE_KEY_STRONG setting should not be set on a mobile device.' )                        
        elif self.encryption_method == 'weak':
            defaults = {'help_text': kwargs.get('help_text', '') + ' (Encryption: weak)'}

            # load public key, private key (if available) and set writer
            if not hasattr(settings, 'PUBLIC_KEY_WEAK'):
                raise ImproperlyConfigured('For \'weak\' security, you must set the PUBLIC_KEY_WEAK setting to ' \
                                           'point to your public key (path and filename) .')
            self.crypter.public_key = settings.PUBLIC_KEY_STRONG
            if 'PRIVATE_KEY_WEAK' in dir(settings):
                # medium security expects a private key to be available on the device, 
                # but you could remove move it to fully de-identify the DB
                if settings.PRIVATE_KEY_WEAK:
                    self.crypter.private_key = settings.PRIVATE_KEY_WEAK     
        if self.encryption_method == 'hash':
            raise ImproperlyConfigured('EncryptedField field \'encryption_method\' \'%s\' is ' \
                                       'not supported yet' % (self.encryption_method ,))    
        kwargs.update(defaults)                    
        super(BaseEncryptedField, self).__init__(*args, **kwargs)

    def get_internal_type(self):
        return "TextField"
    
    def to_python(self, value):
        """ return the decrypted value if a private key is found, otherwise remains encrypted. """
        if isinstance(value, basestring):
            retval = self.crypter.decrypt(value)
        else:
            retval = value
        return retval
    
    def get_prep_value(self, value):
        if value:
            value = self.crypter.encrypt(value)   
        return super(BaseEncryptedField, self).get_prep_value(value)

    def get_db_prep_value(self, value, connection, prepared=False):
        
        """ We ONLY store the hash in the model field. 
        
        The Crypter class will update the Crypt cipher lookup table with
        the hash, cipher pair for future access to the cipher
        
        """ 
        # need to read the docs a bit more as i might be able to just set prepared=True, etc
        # https://docs.djangoproject.com/en/dev/howto/custom-model-fields/#converting-query-values-to-database-values
        if value:
            # call super (which will call get_prep_value)
            encrypted_value = super(BaseEncryptedField, self).get_db_prep_value(value, connection, prepared)
            # update cipher lookup table
            self.crypter.update_cipher_lookup(encrypted_value)
            # remove the cipher prefix and the cipher_text from the value
            # just before the save to the DB
            hash_text = self.crypter.prefix + self.crypter.get_hash(encrypted_value)
            value = hash_text
        return value
    
    def south_field_triple(self):
        "Returns a suitable description of this field for South."
        # We'll just introspect the _actual_ field.
        from south.modelsinspector import introspector
        field_class = "django.db.models.fields.TextField"
        args, kwargs = introspector(self)
        # That's our definition!
        return (field_class, args, kwargs)


