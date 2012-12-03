import socket
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.db.models import get_model


class Base(object):

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
            ``server_device_id``: settings.DEVICE_ID for server (default='99')
            """
        self._using_source = None
        self._using_destination = None
        self._producer = None
        self.server_device_id = kwargs.get('server_device_id', '99')
        self.exception = kwargs.get('exception', TypeError)
        #if not 'ALLOW_DISPATCH' in dir(settings):
        #    raise self.exception('Settings attribute \'ALLOW_DISPATCH\' not found (ALLOW_DISPATCH=<TRUE/FALSE>). Please add to your settings.py.')
        #if not 'DISPATCH_MODEL' in dir(settings):
        #    raise self.exception('Settings attribute \'DISPATCH_MODEL\' not found where DISPATCH_MODEL=(app_label, model_name). Please add to your settings.py.')
        if using_source == using_destination:
            raise self.exception('Arguments \'<source>\' and \'<destination\'> cannot be the same. Got \'{0}\' and \'{1}\''.format(using_source, using_destination))
        self.set_using_source(using_source)
        self.set_using_destination(using_destination)
        self.set_producer()

    def set_using_source(self, using_source=None):
        """Sets the ORM `using` parameter for data access on the "source"."""
        if not using_source:
            raise self.exception('Parameters \'using_source\' cannot be None')
        if using_source not in ['server', 'default']:
            raise self.exception('Argument \'<using_source\'> must be either \'default\' (if run from server) or \'server\' if not run from server.')
        if settings.DEVICE_ID == self.server_device_id and using_source != 'default':
            raise self.exception('Argument \'<using_source\'> must be \'default\' if running on the server (check settings.DEVICE).')
        if settings.DEVICE_ID != self.server_device_id and using_source == 'default':
            raise self.exception('Argument \'<using_source\'> must be \'server\' if running a device (check settings.DEVICE).')
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
            raise self.exception('Parameters \'using_destination\' cannot be None')
        if using_destination == 'server':
            raise self.exception('Argument \'<using_destination\'> cannot be \'server\'.')
        if settings.DEVICE_ID == self.server_device_id and using_destination == 'default':
            raise self.exception('Argument \'<using_destination\'> cannot be \'default\' if running on the server (check settings.DEVICE).')
        if self.is_valid_using(using_destination, 'destination'):
            self._using_destination = using_destination
#        if self.get_using_source() == 'default':
#            # when source is default (running on server), destination must be an active producer settings key
#            if not using_destination in Producer.objects.using(self.get_using_source()).filter(is_active=True).values_list('settings_key'):
#                raise self.exception("Destination {0} does not match any database settings keys of the active producers".format(using_destination))

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

    def set_producer(self):
        """Sets the instance of the current producer based on the ORM `using` parameter for the destination
        and refreshes the list of dispatched Dispatch models.

        .. note:: The producer must always exist on the source. If dispatching via the device, try to
                  find a producer with the settings_key of the format ``DEVICE_HOSTNAME-DBNAME``
                  where DBNAME is the NAME attribute of the ``default`` DATABASE on the device."""
        Producer = get_model('bhp_sync', 'Producer')
        # try to determine producer from using_destination
        if self.get_using_destination() == 'default':
            # try to find the producer on the server with hostname + database name
            settings_key = '{0}-{1}'.format(socket.gethostname().lower(), settings.DATABASES.get('default').get('NAME'))
            if Producer.objects.using(self.get_using_source()).filter(settings_key=settings_key).exists():
                self._producer = Producer.objects.using(self.get_using_source()).get(settings_key=settings_key)
        else:
            if Producer.objects.using(self.get_using_source()).filter(settings_key=self.get_using_destination()).exists():
                self._producer = Producer.objects.using(self.get_using_source()).get(settings_key=self.get_using_destination())
        if not self._producer:
            raise TypeError('Dispatcher cannot find producer with settings key {0} on the source {1}.'.format(self.get_using_destination(), self.get_using_source()))
        # check the producers DATABASES key exists
        # TODO: what if producer is "me", e.g settings key is 'default'
        if not self.get_using_destination() == 'default':
            settings_key = self._producer.settings_key
            if not [dbkey for dbkey in settings.DATABASES.iteritems() if dbkey[0] == settings_key]:
                raise ImproperlyConfigured('Dispatcher expects settings attribute DATABASES to have a NAME '
                                           'key to the \'producer\'. Got name=\'{0}\', settings_key=\'{1}\'.'.format(self._producer.name, self._producer.settings_key))

    def get_producer(self):
        """Returns an instance of the current producer."""
        if not self._producer:
            self.set_producer()
        return self._producer
