import socket
import re
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from bhp_variables.models import StudySpecific


class Device(object):

    """ Determines the device name, useful to know when identifiers are created by the device.

    :usage:
        >>> device = Device()
        >>> device.get_device_id()
        >>> 31

    * First tries settings.py (with DEVICE_ID settings attribute),
    * then hostname (with HOSTNAME_PREFIX settings attribute),
    * then from the DB.

    Settings attribute DEVICE_ID_LENGTH, if exists, determines the number of digits of the device_id. """

    def __init__(self, **kwargs):

        """ Set length and pattern of device_id and call update(). """

        # if settings attribute DEVICE_ID_LENGTH exists, use that value
        self._device_id = None
        self.length = None
        if 'DEVICE_ID_LENGTH' in dir(settings):
            self.length = settings.DEVICE_ID_LENGTH
        if not self.length:
            self.length = 2
        # set re pattern to a sequence of digits where the first digit cannot be 0
        self.pattern = r'[1-9]{1}[0-9]{' + str(self.length - 1) + '}$'
        #self._update()

    @property
    def device_id(self):
        return self.get_device_id()

    def get_device_id(self):
        if not self._device_id:
            self.set_device_id()
        return self._device_id

    def set_device_id(self, value=None):
        if value:
            raise TypeError('Device id cannot be set dynamically.')
        self._device_id = self._update()

    def _update(self):
        # try to get device_id from settings first
        if not self._update_from_settings():
            # then try from hostname
            if not self._update_from_hostname():
                # then try the DB
                if not self._update_from_db():
                    # if still not found, raise an error
                    raise ImproperlyConfigured('Cannot determine the \'device_id\' for this device. This should be set in settings.py, extracted from the hostname, or entered as a DB variable')
        return self._device_id

    def _update_from_settings(self):
        """ Gets device_id from settings.py. """
        attr = 'DEVICE_ID'
        if attr in dir(settings):
            if re.match(self.pattern, getattr(settings, attr)):
                self._device_id = getattr(settings, attr)
            else:
                ImproperlyConfigured('Incorrect format for settings attribute DEVICE_ID. Got {device_id}'.format(device_id=getattr(settings, attr)))
        return self._device_id

    def _update_from_hostname(self, hostname_prefix=None):
        """ Gets device device_id from hostname using the hostname prefix and the regex/length. """
        attr = 'HOSTNAME_PREFIX'
        if attr in dir(settings):
            hostname_prefix = getattr(settings, attr)
            hostname = socket.gethostname()
            if not re.match(self.pattern, hostname[len(hostname) - self.length:]):
                raise ImproperlyConfigured("Cannot determine DEVICE_ID from hostname {hostname} \
                                        given prefix {prefix}".format(hostname=hostname,
                                                                      prefix=hostname_prefix))
            self._device_id = hostname[len(hostname) - self.length:]
        return self._device_id

    def _update_from_db(self):
        """ Gets device device_id from the db. """
        study_specific = StudySpecific.objects.all()[0]
        device_id = study_specific.device_id
        if not device_id:
            raise ImproperlyConfigured("Cannot determine DEVICE_ID from DB. Got None or 0.")
        if not re.match(self.pattern, device_id):
            ImproperlyConfigured('Incorrect format for DEVICE_ID. Got {device_id}'.format(device_id=device_id))
        self._device_id = device_id
        return self._device_id
