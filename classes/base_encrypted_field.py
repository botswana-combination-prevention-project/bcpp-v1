from django.db import models

from crypter import Crypter


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
    description = 'Field to encrypt and decrypt values that are stored \
                   as encrypted'
    __metaclass__ = models.SubfieldBase

    def __init__(self, *args, **kwargs):
        """
        The required field attribute 'encryption_method' guides in loading
        public and private keys

        1. restricted key-pair: use on values that should be less convenient
           to decrypt. Private key is not
           allowed on mobile devices (settings.IS_SECURE_DEVICE).
        2. local key-pair: same as restricted key-pair but the private key
           is expected to be available and is not checked for """
        self.crypter = Crypter()
        self.crypter.algorithm = self.algorithm
        if self.algorithm not in self.crypter.VALID_MODES.keys():
            raise KeyError('Invalid algorithm \'{algorithm}\'. '
                           'Must be one of {keys}'.format(algorithm=self.algorithm,
                                                          keys=', '.join(self.crypter.VALID_MODES.keys())))
        self.crypter.mode = self.mode
        if (self.mode not in
            self.crypter.VALID_MODES.get(self.algorithm).iterkeys()):
            raise KeyError('Invalid mode \'{mode}\' for algorithm {algorithm}.'
                           ' Must be one of {keys}'
                           .format(
                                mode=self.mode,
                                algorithm=self.algorithm,
                                keys=', '.join(self.crypter.VALID_MODES.get(self.algorithm).keys())))
        # set the db field length based on the hash
        defaults = {'max_length': self.crypter.hasher.length +
            len(self.crypter.HASH_PREFIX) + len(self.crypter.SECRET_PREFIX)}
        kwargs.update(defaults)
        super(BaseEncryptedField, self).__init__(*args, **kwargs)

    def have_decryption_key(self):
        """ """
        retval = False
        if self.crypter.private_key:
            retval = True
        return retval

    def get_public_keyfile(self):
        return self.crypter.VALID_MODES.get(
            self.algorithm).get(self.mode).get('public')

    def get_private_keyfile(self):
        return self.crypter.VALID_MODES.get(
            self.algorithm).get(self.mode).get('private')

    def is_encrypted(self, value):
        """ wrap the crypter method of same name """
        return self.crypter.is_encrypted(value)

    def decrypt(self, value, **kwargs):
        """ wrap the crypter method of same name """
        return self.crypter.decrypt(value)

    def encrypt(self, value, **kwargs):
        """ wrap the crypter method of same name """
        return self.crypter.encrypt(value)

    def validate_with_cleaned_data(self, attname, cleaned_data):
        """ May be overridden to test field data against other values
        in cleaned data.

        Should raise a forms.ValidationError if the test fails

        1. 'attname' is the key in cleaned_data for the value to be tested,
        2. 'cleaned_data' comes from django.forms clean() method """
        pass

    def to_python(self, value):
        """ Returns the decrypted value IF the private key is found,
        otherwise returns the encrypted value. """
        if isinstance(value, basestring):
            retval = self.decrypt(value)
            self.readonly = retval is not value
        else:
            retval = value
        return retval

    def get_prep_value(self, value):
        """ Always returns the encrypted value. """
        if value:
            value = self.encrypt(value)
        return super(BaseEncryptedField, self).get_prep_value(value)

    def get_db_prep_value(self, value, connection, prepared=False):
        """ Store the hash in the model field and the secret in the
        lookup table (Crypt). """

        # TODO(erikvw): need to read the docs a bit more as i might be able to
        #     just set prepared=True, etc
        #     https://docs.djangoproject.com/en/dev/howto/custom-model-
        #     fields/#converting-query-values-to-database-values
        if value:
            # call super (which will call get_prep_value)
            hash_secret = super(BaseEncryptedField, self).get_db_prep_value(
                                                              value,
                                                              connection,
                                                              prepared)
            # switch the returned value from value to hash
            # because we store the hash, not the value or secret
            hash_text = self.crypter.get_db_prep_value(hash_secret)
            value = hash_text
        return value

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
