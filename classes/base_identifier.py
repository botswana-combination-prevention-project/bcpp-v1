import re
from django.db.models import get_model
from django.conf import settings
from bhp_device.classes import Device
from check_digit import CheckDigit


class BaseIdentifier(object):

    def get_identifier_prep(self):
        """ Users may override to pass non-default keyword arguments to get_identifier
        before the identifier is created."""
        options = {}
        return options

    def get_identifier_post(self):
        """ Users may override to run something after the identifier is created."""
        return

    def _prepare_identifier(self, options, **kwargs):
        """Calls user method self.get_identifier_prep() and adds/updates custom options to the defaults."""
        custom_options = self.get_identifier_prep(**kwargs)
        for k, v in custom_options.iteritems():
            options.update({k: v})
        return options

    def _post_identifier(self, identifier, **kwargs):
        self.get_identifier_post(identifier, **kwargs)
        return None

    def get_identifier(self, add_check_digit=True, **kwargs):
        """ Returns a formatted identifier based on the identifier format and the dictionary
        of options.

        Calls self._prepare_identifier()

        Arguments:
          add_check_digit: if true adds a check digit calculated using the numbers in the
            identifier. Letters are stripped out if they exist. (default: True)

        Keyword Arguments:
          * app_name: app_label for model_name below. (default: 'bhp_identifier')
            model_name: lower case of model.object_name to use to track subject identifiers
            as they are created. id of this model is the sequence integer.
            (default: 'subject_identifier')
          * site: site code. (default: '')
          * seed: not used
          * padding: integer to calculate right justified padding on the sequence segement
            of the identifier. (default: 4)
          * modulus: used to calculate the check digit. (default: 7)
          * prefix: prefix for identifier such as the protocol number (e.g 041, 056 etc).
            (default: (default: settings.PROJECT_IDENTIFIER_PREFIX)
          * identifier_format: template for the identifier with keywords referring to the above keys.
            (default: '{prefix}-{site}{device_id}{sequence}')
          """
        options = {}
        # set default options
        add_check_digit = options.pop('add_check_digit', True)
        options.update('app_name', 'bhp_identifier')
        options.update('model_name', 'subject_identifier')
        options.update('site', '')
        options.update('padding', 4)
        options.update('seed', 0)
        options.update('modulus', settings.PROJECT_IDENTIFIER_MODULUS)
        options.update('prefix', settings.PROJECT_IDENTIFIER_PREFIX)
        options.update('identifier_format', "{prefix}-{site}{device_id}{sequence}")
        # check for custom options
        options = self._prepare_identifier(options, **kwargs)
        # use and pop key/values that are obviously not needed by format()
        modulus = options.pop('modulus')
        IdentifierModel = get_model(options.pop('app_name'), options.pop('model_name'))
        identifier_model = IdentifierModel.objects.create(seed=options.pop('seed'), padding=options.pop('padding'))
        options.update(sequence=identifier_model.sequence)
        identifier_format = options.pop('identifier_format')
        device = Device()
        options.update(device_id=device.device_id)
        try:
            base = identifier_format.format(**options)
        except KeyError:
            raise KeyError('Missing key/pair for identifier format. '
                           'Got format {0} with dictionary {1}'.format(identifier_format, options))
        # add a check digit base on the integers in the identifier
        if add_check_digit:
            check_digit = CheckDigit()
            new_identifier = "{base}-{check_digit}".format(
                             base=base,
                             check_digit=check_digit.calculate(int(re.search('\d+', base).group(0)), modulus))
            identifier_model.identifier = new_identifier
        # update the identifier instance
        identifier_model.save()
        # call custom post method
        self._post_identifier(new_identifier, **kwargs)
        return new_identifier
