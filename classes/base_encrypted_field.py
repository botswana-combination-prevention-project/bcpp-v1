from django.db import models
from django.core.exceptions import ImproperlyConfigured
from crypter import Crypter


class BaseEncryptedField(models.Field):
    
    """ A field class that stores sensitive data in an encrypted format.
    
    To maintain uniqueness and searchability, only the hash is ever stored in the model field.
    
    If a cipher is generated, it is stored with the hash in the Crypt lookup model and will be
    made available when required for decryption (e.g. the private key is available)
       
    Hash salt, public key and private key are referred to via the settings file
    
    """

    description = "Field to encrypt and decrypt values that are stored as encrypted"
    __metaclass__ = models.SubfieldBase
    valid_encryption_methods = ['restricted key-pair', 'local key-pair', 'hash-only']
    
    def __init__(self, *args, **kwargs):  
        """
        The required field attribute 'encryption_method' guides in loading public and private keys
        
        1. restricted key-pair: use on values that should be less convenient to decrypt. Private key is not
           allowed on mobile devices (settings.IS_SECURE_DEVICE).
        2. local key-pair: same as restricted key-pair but the private key is expected to be available and is not checked for
        3. hash: irreversibly hash the value. do not create a corresponding cipher 
        """
        self.crypter = Crypter()

        defaults = {}
        
        self.encryption_method = kwargs.get('encryption_method', None)
        
        if 'encryption_method' in kwargs:
            del kwargs['encryption_method']
        
        if self.encryption_method not in self.valid_encryption_methods:
            raise ImproperlyConfigured('Available options for EncryptedField field parameter' \
                                        '\'encryption_method\' are \'%s\'. Got \'%s\' ' \
                                        % ('\' or \''.join(self.valid_encryption_methods), kwargs.get('encryption_method')))
           
        if self.encryption_method == 'hash-only':
            raise ImproperlyConfigured('EncryptedField field \'encryption_method\' \'%s\' is ' \
                                       'not supported yet' % (self.encryption_method ,))    
        kwargs.update(defaults)                    
                
        self.crypter.set_public_key(self.get_public_keyfile())

        self.crypter.set_private_key(self.get_private_keyfile())
        
        super(BaseEncryptedField, self).__init__(*args, **kwargs)

    def get_public_keyfile(self, keyfile=None):
        raise ImproperlyConfigured("method should be overridden")
        
    def get_private_keyfile(self, keyfile=None):
        raise ImproperlyConfigured("method should be overridden")
    
    #    def set_private_key(self):
    #        self.crypter.set_private_key(self.get_private_keyfile())
    #
    #    def set_public_key(self):
    #        self.crypter.set_public_key(self.get_public_keyfile())

    def get_internal_type(self):
        return "CharField"
    
    def is_encrypted(self, value):
        return self.crypter.is_encrypted(value)
    
    def decrypt(self, value):
        return self.crypter.decrypt(value)
    
    def validate_with_cleaned_data(self, attname, cleaned_data):
        
        """ may be overridden to test field data against other values in cleaned data. 
        
        Should raise a forms.ValidationError if the test fails 
        
        1. 'attname' is the key in cleaned_data for the value to be tested, 
        2. 'cleaned_data' comes from django.forms clean() method
        
        """
        pass
    
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


