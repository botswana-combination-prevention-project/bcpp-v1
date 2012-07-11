from django.db import models
from django.core.exceptions import ImproperlyConfigured
from crypter import Crypter


class BaseEncryptedField(models.Field):
    
    """ A base field class to store sensitive data in an encrypted format.
    
    * To maintain uniqueness and searchability, only the hash is ever stored in the model field.
    * The cipher is stored with the hash in the Crypt cipher lookup model and will be
      made available when required for decryption (e.g. the private key is available)
    * Salt, public key filename and private key filename are referred to via the settings file """

    # see https://docs.djangoproject.com/en/dev/howto/custom-model-fields/#the-subfieldbase-metaclass 
    description = "Field to encrypt and decrypt values that are stored as encrypted"
    __metaclass__ = models.SubfieldBase
    # can only set encryption_method to these values at the model field 
    valid_encryption_methods = ['restricted RSA key-pair', 'local RSA key-pair', 'local AES']
    
    def __init__(self, *args, **kwargs):  
        """
        The required field attribute 'encryption_method' guides in loading public and private keys
        
        1. restricted key-pair: use on values that should be less convenient to decrypt. Private key is not
           allowed on mobile devices (settings.IS_SECURE_DEVICE).
        2. local key-pair: same as restricted key-pair but the private key is expected to be available and is not checked for
        """
        # this has all the crypto methods
        self.crypter=Crypter() 
        self.crypter.algorithm=self.algorithm
        if self.mode not in self.crypter.files.iterkeys():
            raise KeyError('Invalid mode \'{mode}\' for algorithm {algorithm}. Must be one of {keys}'.format(mode=self.mode, algorithm=self.algorithm, keys=', '.join([key for key in self.crypter.files.iterkeys()])))
        else:
            self.crypter.mode=self.mode
        # check encryption_method kwarg from subclass or field object
        self.encryption_method = self.check_encryption_method(kwargs.get('encryption_method', None))        
        if 'encryption_method' in kwargs:
            del kwargs['encryption_method']                 
        # set the field length based on the hash
        defaults = {'max_length': self.crypter.hasher.length+len(self.crypter.prefix)+len(self.crypter.cipher_prefix)}
        kwargs.update(defaults)
        #get public and private keys for Crypter()
        self.crypter.set_public_key(self.get_public_keyfile())
        self.crypter.set_private_key(self.get_private_keyfile())
        self.crypter.set_aes_key(self.get_aes_key())
        super(BaseEncryptedField, self).__init__(*args, **kwargs)    
    
    @property
    def extra_salt(self):
        """salt for hashes"""
        if not self.algorithm:
            raise ImproperlyConfigured('Encryption algorithm cannot be None')
        if not self.mode:
            raise ImproperlyConfigured('Encryption mode cannot be None')
        return self.algorithm+self.mode.replace(' ', '')
    
    def get_aes_key(self, key=None):
        """ Override to return the aes key """
        return ''
    
    def get_public_keyfile(self, keyfile=None):
        """ Override to return the key filename and path if not in the project root """
        raise ImproperlyConfigured("method should be overridden")
        
    def get_private_keyfile(self, keyfile=None):
        """ Override to return the key filename and path if not in the project root """
        raise ImproperlyConfigured("method should be overridden")
    
    def is_encrypted(self, value):
        """ wrap the crypter method of same name """
        return self.crypter.is_encrypted(value)
    
    def decrypt(self, value, **kwargs):
        """ wrap the crypter method of same name """
        return self.crypter.decrypt(value, extra_salt=self.extra_salt)
    
    def encrypt(self, value, **kwargs):
        """ wrap the crypter method of same name """   
        return self.crypter.encrypt(value, extra_salt=self.extra_salt)
    
    def validate_with_cleaned_data(self, attname, cleaned_data):
        """ May be overridden to test field data against other values in cleaned data. 
        
        Should raise a forms.ValidationError if the test fails 
        
        1. 'attname' is the key in cleaned_data for the value to be tested, 
        2. 'cleaned_data' comes from django.forms clean() method """
        pass
    
    def to_python(self, value):
        """ Returns the decrypted value IF the private key is found, otherwise returns the encrypted value. """
        if isinstance(value, basestring):
            retval = self.decrypt(value)
            self.readonly = retval==value
        else:
            retval = value
        return retval
    
    def get_prep_value(self, value):
        """ Always returns the encrypted value. """
        if value:
            value = self.encrypt(value)   
        return super(BaseEncryptedField, self).get_prep_value(value)

    def get_db_prep_value(self, value, connection, prepared=False):
        """ Store the hash in the model field and the cipher in the lookup table (Crypt). """ 
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
    
    def get_internal_type(self):
        """This is a Charfield as we only ever store the hash, which is a fixed length. """
        return "CharField"
    
    def south_field_triple(self):
        "Returns a suitable description of this field for South."
        # We'll just introspect the _actual_ field.
        from south.modelsinspector import introspector
        field_class = "django.db.models.fields.CharField"
        args, kwargs = introspector(self)
        # That's our definition!
        return (field_class, args, kwargs)

    def check_encryption_method(self, encryption_method):
        """ Check if the subclass or model field pass a valid encryption method."""
        if encryption_method not in self.valid_encryption_methods:
            raise ImproperlyConfigured('Available options for EncryptedField field parameter' \
                                        '\'encryption_method\' are \'%s\'. Got \'%s\' ' \
                                        % ('\' or \''.join(self.valid_encryption_methods), encryption_method))
            
