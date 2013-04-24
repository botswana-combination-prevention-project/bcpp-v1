import re
import uuid
from django.core.exceptions import ImproperlyConfigured
from django.db.models import get_model
from django.conf import settings
from bhp_device.classes import Device
from bhp_identifier.exceptions import IdentifierError, IndentifierFormatError
from check_digit import CheckDigit


class BaseIdentifier(object):
    """ Base class for all identifiers."""

    def __init__(self, identifier_format=None, app_name=None, model_name=None, site_code=None, padding=None, modulus=None, identifier_prefix=None, using=None):
        self.identifier_format = None
        self.app_name = None
        self.model_name = None
        self.padding = None
        self.modulus = None
        self.identifier_prefix = None
        self.site_code = None
        self.using = using
        if 'PROJECT_IDENTIFIER_PREFIX' not in dir(settings):
            raise ImproperlyConfigured('Missing settings attribute PROJECT_IDENTIFIER_PREFIX. Please add. For example, PROJECT_IDENTIFIER_PREFIX = \'041\' for project BHP041.')
        if 'PROJECT_IDENTIFIER_MODULUS' not in dir(settings):
            modulus = modulus or 7
        self.identifier_format = identifier_format or "{prefix}-{site_code}{device_id}{sequence}"
        self.app_name = app_name or 'bhp_identifier'
        self.model_name = model_name or 'subjectidentifier'
        self.padding = padding or 4
        self.modulus = modulus or settings.PROJECT_IDENTIFIER_MODULUS
        self.identifier_prefix = identifier_prefix or settings.PROJECT_IDENTIFIER_PREFIX
        self.site_code = site_code or ''
        # confirm identifier tracking model exists
        if not get_model(self.app_name, self.model_name):
            raise ImproperlyConfigured('Identifier tracking model with app_name={0} and model_name={1} does not exist.'.format(self.app_name, self.model_name))

    def get_identifier_prep(self, **kwargs):
        """ Users may override to pass non-default keyword arguments to get_identifier
        before the identifier is created."""
        return {}

    def get_identifier_post(self, identifier, **kwargs):
        """ Users may override to run something after the identifier is created.

        Must return the identifier."""
        return identifier

    def _get_identifier_prep(self, **kwargs):
        """Calls user method self.get_identifier_prep() and adds/updates custom options to the defaults."""
        device = Device()
        options = {'identifier_prefix': self.identifier_prefix,
                   'site_code': self.site_code,
                   }
        options.update(device_id=device.get_device_id())
        custom_options = self.get_identifier_prep(**kwargs)
        if not isinstance(custom_options, dict):
            raise IdentifierError('Expected a dictionary from method get_identifier_prep().')
        if not self.identifier_format:
            raise AttributeError('Attribute identifier_format may not be None.')
        for k, v in custom_options.iteritems():
            if k not in self.identifier_format:
                raise IndentifierFormatError('Unexpected keyword {0} for identifier format {1}'.format(k, self.identifier_format))
            options.update({k: v})
        return options

    def _get_identifier_post(self, identifier, **kwargs):
        """Must return the identifier."""
        identifier = self.get_identifier_post(identifier, **kwargs)
        return identifier

    def add_check_digit(self, base_new_identifier):
        """Adds a check digit base on the integers in the identifier."""
        check_digit = CheckDigit()
        return "{base}-{check_digit}".format(
            base=base_new_identifier,
            check_digit=check_digit.calculate(int(re.search('\d+', base_new_identifier.replace('-', '')).group(0)), self.modulus))

    def get_identifier(self, add_check_digit=True, is_derived=False, **kwargs):
        """ Returns a formatted identifier based on the identifier format and the dictionary
        of options.

        Calls self._get_identifier_prep()

        Arguments:
          add_check_digit: if true adds a check digit calculated using the numbers in the
            identifier. Letters are stripped out if they exist. (default: True)
          is_derived: identifier is derived from an existing identifier so get a sequence
            from the identifier_model. For example, an infant identifier is derived from the
            maternal identifier. (default: False)

        Keyword Arguments:
          * app_name: app_label for model_name below. (default: 'bhp_identifier')
            model_name: lower case of model.object_name to use to track subject identifiers
            as they are created. id of this model is the sequence integer.
            (default: 'subject_identifier')
          * site_code: site code. (default: '')
          * seed: not used
          * padding: integer to calculate right justified padding on the sequence segement
            of the identifier. (default: 4)
          * modulus: used to calculate the check digit. (default: 7)
          * identifier_prefix: prefix for identifier such as the protocol number (e.g 041, 056 etc).
            (default: (default: settings.PROJECT_IDENTIFIER_PREFIX)
          * identifier_format: template for the identifier with keywords referring to the above keys.
            (default: '{identifier_prefix}-{site_code}{device_id}{sequence}')
          """
        # update the format options dictionary
        options = self._get_identifier_prep(**kwargs)
        # check if this identifier is to be derived from an existing identifier
        if not is_derived:
            IdentifierModel = get_model(self.app_name, self.model_name)
            # put a random uuid temporarily in the identifier field
            # to maintain unique constraint on identifier field.
            self.identifier_model = IdentifierModel.objects.using(self.using).create(identifier=str(uuid.uuid4()), padding=self.padding)
            options.update(sequence=self.identifier_model.sequence)
        else:
            # the identifier is derived from an existing one. no need for
            # a sequence, therefore no need for the identifier_model
            self.identifier_model = None
            options.update(sequence='')
        # apply options to format to create a formatted identifier
        try:
            new_identifier = self.identifier_format.format(**options)
        except KeyError:
            raise IndentifierFormatError('Missing key/pair for identifier format. '
                'Got format {0} with dictionary {1}. Either correct the identifier '
                'format or provide a value for each place holder in the identifier format.'.format(self.identifier_format, options))
        # check if adding a check digit
        if add_check_digit:
            new_identifier = self.add_check_digit(new_identifier)
        # call custom post method
        new_identifier = self._get_identifier_post(new_identifier, **kwargs)
        if not new_identifier:
            raise IdentifierError('Identifier cannot be None. Confirm overridden methods return the correct value. See BaseSubjectIdentifier')
        # update the identifier model
        if self.identifier_model:
            self.identifier_model.identifier = new_identifier
            self.identifier_model.save(using=self.using)
        return new_identifier
