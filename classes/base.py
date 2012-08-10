import re
from django.db.models import get_model
from django.conf import settings
from bhp_device.classes import Device
from check_digit import CheckDigit


class Base(object):

    def __init__(self, *args, **kwargs):

        # the instance, if set, will be updated instead of creating a new instance
        self.registered_subject = None
        # need an instance of the consent, raise an error later if not available
        self.consent = None

    def _consent_required(self):
        return True

    def get_identifier_prep(self):
        """ Users may override to pass non-default keyword arguments to get_identifier.

        See _prepare_identifier for list of allowed Keyword Arguments."""
        options = {}
        return options

    def _prepare_identifier(self):
        options = self.get_identifier_prep()
        allowed_keys = ['seed', 'padding', 'site', 'app_name', 'model_name', 'identifier_format', 'modulus', 'prefix']
        diff = set(options.keys()).difference(allowed_keys)
        if diff:
            raise KeyError('Invalid keyword argument(s) {0}.'.format(' ,'.join(diff)))
        return options

    def get_identifier(self):
        """ Returns a formatted identifier."""
        options = self._prepare_identifier()
        app_name = options.get('app_name', 'bhp_identifier')
        model_name = options.get('model_name', 'subject_identifier')
        site = options.get('site', '')
        padding = options.get('padding', 4)
        seed = options.get('seed', 0)
        identifier_format = options.get('identifier_format', "{prefix}-{site}{device_id}{sequence}")
        modulus = options.get('modulus', 7)
        prefix = options.get('prefix', settings.PROJECT_IDENTIFIER_PREFIX)
        IdentifierModel = get_model(app_name, model_name)
        identifier_model = IdentifierModel.objects.create(seed=seed, padding=padding)
        device = Device()
        base = identifier_format.format(prefix=prefix,
                             site=site,
                             device_id=device.device_id,
                             sequence=identifier_model.sequence)
        # add a check digit base on the integers in the identifier
        check_digit = CheckDigit()
        new_identifier = "{base}-{check_digit}".format(
                             base=base,
                             check_digit=check_digit.calculate(int(re.search('\d+', base).group(0)), modulus))
        # re-save the Identifier model instance
        identifier_model.identifier = new_identifier
        identifier_model.save()
        return new_identifier

    def update_register(self, consent, attrname='subject_identifier', **kwargs):
        """ update for this subject in registered subject """
        # the model, for creating a new instance
        self.RegisteredSubject = get_model('bhp_registration', 'registeredsubject')
        # access registered subject manager method
        self.RegisteredSubject.objects.update_with(consent, attrname, **kwargs)
