from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from bhp_using.exceptions import UsingError, UsingSourceError, UsingDestinationError


class BaseUsing(object):

    def __init__(self, using_source, using_destination, **kwargs):
        """Initializes and verifies arguments ``using_source`` and ``using_destination``.

        Args:
            ``using_source``: settings.DATABASE key for source. Source is the server so must
                          be 'default' if running on the server and 'server'
                          if running on the device.
            ``using_destination``: settings.DATABASE key for destination. If running from the server
                               this key must exist in settings.DATABASES. If on the device, must be 'default'.
                               In either case, ``using_destination`` must be found in the
                               source :class:`Producer` model as producer.settings_key (see :func:`set_producer`.)

        Keywords:
            ``server_device_id``: settings.DEVICE_ID for server (default='99')"""
        self._using_source = None
        self._using_destination = None
        self.server_device_id = kwargs.get('server_device_id', '99')
        if using_source == using_destination:
            raise UsingError('Arguments \'<source>\' and \'<destination\'> cannot be the same. Got \'{0}\' and \'{1}\''.format(using_source, using_destination))
        self.set_using_source(using_source)
        self.set_using_destination(using_destination)

    def set_using_source(self, using_source=None):
        """Sets the ORM `using` parameter for data access on the "source"."""
        if not using_source:
            raise UsingSourceError('Parameters \'using_source\' cannot be None')
        if using_source not in ['server', 'default']:
            raise UsingSourceError('Argument \'<using_source\'> must be either \'default\' (if run from server) or \'server\' if not run from server.')
        if settings.DEVICE_ID == self.server_device_id and using_source != 'default':
            raise UsingSourceError('Argument \'<using_source\'> must be \'default\' if running on the server (check settings.DEVICE).')
        if settings.DEVICE_ID != self.server_device_id and using_source == 'default':
            raise UsingSourceError('Argument \'<using_source\'> must be \'server\' if running a device (check settings.DEVICE).')
        if self.is_valid_using(using_source, 'source'):
            self._using_source = using_source

    def get_using_source(self):
        """Gets the ORM `using` parameter for "source"."""
        if not self._using_source:
            self.set_using_source()
        return self._using_source

    def set_using_destination(self, using_destination=None):
        """Sets the ORM `using` parameter for data access on the "destination"."""
        if not using_destination:
            raise UsingDestinationError('Parameters \'using_destination\' cannot be None')
        if using_destination == 'server':
            raise UsingDestinationError('Argument \'<using_destination\'> cannot be \'server\'.')
        if settings.DEVICE_ID == self.server_device_id and using_destination == 'default':
            raise UsingDestinationError('Argument \'<using_destination\'> cannot be \'default\' if running on the server (check settings.DEVICE).')
        if self.is_valid_using(using_destination, 'destination'):
            self._using_destination = using_destination

    def get_using_destination(self):
        """Gets the ORM `using` parameter for "destination"."""
        if not self._using_destination:
            self.set_using_destination()
        return self._using_destination

    def is_valid_using(self, using, label):
        """Confirms an ORM `using` parameter is valid by checking :file:`settings.py`."""
        if not [dbkey for dbkey in settings.DATABASES.iteritems() if dbkey[0] == using]:
            raise ImproperlyConfigured('Cannot find {1} key \'{0}\' in settings attribute DATABASES. Please add to settings.py.'.format(using, label))
        return True
