from django.db import models
from django.core.exceptions import ValidationError
from field_crypter import FieldCrypter


class BaseEncryptedField(models.Field):

    """ A base field class to store sensitive data at rest in an encrypted
    format.

    * To maintain uniqueness and searchability, only the hash is ever
      stored in the model field.
    * The cipher is stored with the hash in the :class:`bhp_crypto.models.
      Crypt` cipher lookup model and will be
      made available when required for decryption (e.g. the private key is
      available)
    * Salt, public key filename and private key filename are referred to
      via the settings file """

    # see https://docs.djangoproject.com/en/dev/howto/
    #  custom-model-fields/#the-subfieldbase-metaclass
    description = 'Field class that stores values as encrypted'

    __metaclass__ = models.SubfieldBase

    def __init__(self, *args, **kwargs):
        """ """
        self.field_crypter = FieldCrypter(self.algorithm, self.mode)
        # set the db field length based on the hash
        defaults = {'max_length': self.field_crypter.hasher.length +
                                  len(self.field_crypter.crypter.HASH_PREFIX) +
                                  len(self.field_crypter.crypter.SECRET_PREFIX)}
        kwargs.update(defaults)
        super(BaseEncryptedField, self).__init__(*args, **kwargs)

#    def have_decryption_key(self):
#        """ """
#        retval = False
#        if self.field_crypter.private_key:
#            retval = True
#        return retval

    def get_max_length(self):
        return (self.field_crypter.hasher.length + len(self.field_crypter.crypter.HASH_PREFIX) +
               len(self.field_crypter.crypter.SECRET_PREFIX))

    def is_encrypted(self, value):
        """ wrap the crypter method of same name """
        return self.field_crypter.is_encrypted(value)

    def decrypt(self, value, **kwargs):
        """ wrap the crypter method of same name """
        return self.field_crypter.decrypt(value)

    def encrypt(self, value, **kwargs):
        """ wrap the crypter method of same name """
        return self.field_crypter.encrypt(value)

    def validate_with_cleaned_data(self, attname, cleaned_data):
        """ May be overridden to test field data against other values
        in cleaned data.

        Should raise a forms.ValidationError if the test fails

        1. 'attname' is the key in cleaned_data for the value to be tested,
        2. 'cleaned_data' comes from django.forms clean() method """
        pass

    def to_python(self, value):
        """ Returns the decrypted value IF the private key is found, otherwise returns
        the encrypted value.

        Value comes from DB as a hash (e.g. <hash_prefix><hashed_value>). If DB value is being
        acccessed for the first time, value is not an encrypted value (not a prefix+hashed_value)."""
        retval = value
        if value:
            if isinstance(value, basestring):
                if not self.algorithm or not self.mode:
                    raise ValidationError('Algorithm and mode not set for encrypted field')
                # decrypt will check if is_encrypted (e.g. enc1::<hash>)
                retval = self.decrypt(value)
                # if it did not decrypt, set field to read only
                self.readonly = retval is not value
            else:
                # at this point, only handling string types
                raise TypeError('Expected basestring. Got {0}'.format(value))
        return retval

    def get_prep_value(self, value, encrypt=True):
        """ Returns the hashed_value with prefix (or None) and, if needed, updates the secret lookup.

        Keyword arguments:
        encrypt -- if False, the value is returned as is (default True)

        """
        retval = value
        if value and encrypt:
            encrypted_value = self.encrypt(value)
            retval = self.field_crypter.get_prep_value(encrypted_value, value)
        return retval

    def get_prep_lookup(self, lookup_type, value):
        """ Only decrypts the stored value to handle 'exact' and 'in'
        but excepts 'icontains' as if it is 'exact' so that the admin
        search fields work.

        Also, 'startswith' does not decrypt and may only be used to check for the hash_prefix.
        All others are errors.
        """
        if lookup_type == 'exact' or lookup_type == 'icontains':
            return self.get_prep_value(value)
        elif lookup_type == 'isnull':
            if type(value) != bool:
                raise TypeError(('Value for lookup type \'{0}\' must be a boolean '
                                 'for fields using encryption. Got {1}').format(lookup_type, value))
            return self.get_prep_value(value, encrypt=False)
        elif lookup_type == 'startswith':
            # allow to test field value for the hash_prefix only, NO searching on the hash
            if value != self.field_crypter.crypter.HASH_PREFIX:
                raise TypeError(('Value for lookup type {0} may only be \'{1}\' for '
                                 'fields using encryption.').format(lookup_type,
                                                                    self.field_crypter.crypter.HASH_PREFIX))
            return self.get_prep_value(value, encrypt=False)
        elif lookup_type == 'in':
            return [self.get_prep_value(v) for v in value]
        else:
            raise TypeError('Lookup type %r not supported.' % lookup_type)

    def get_internal_type(self):
        """This is a Charfield as we only ever store the hash, which is a \
        fixed length char. """
        return "CharField"

    def south_field_triple(self):
        "Returns a suitable description of this field for South."
        # We'll just introspect the _actual_ field.
        from south.modelsinspector import introspector
        field_class = "django.db.models.fields.CharField"
        args, kwargs = introspector(self)
        # That's our definition!
        return (field_class, args, kwargs)
