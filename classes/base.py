from django.conf import settings
from django.core.exceptions import ImproperlyConfigured


class Base(object):

    def __init__(self, **kwargs):
        self._using_source = None
        self.using_destination = None
        self.exception = kwargs.get('exception', TypeError)

    def set_using_source(self, using_source=None):
        if not using_source:
            raise self.exception('Parameters \'using_source\' cannot be None')
        if using_source not in ['server', 'default']:
            raise self.exception('Argument \'<using_source\'> must be either \'default\' (if run from server) or \'server\' if not run from server.')
        if settings.DEVICE_ID == '99':
            raise self.exception('Argument \'<using_source\'> must be \'default\' if running on the server (settings.DEVICE=99).')
        if self.is_valid_using(using_source, 'source'):
            self._using_source = using_source

    def get_using_source(self):
        if not self._using_source:
            self.set_using_source()
        return self._using_source

    def set_using_destination(self, using_destination=None):
        if not using_destination:
            raise self.exception('Parameters \'using_destination\' cannot be None')
        if using_destination == 'server':
            raise self.exception('Argument \'<using_destination\'> cannot be \'server\'.')
        if settings.DEVICE_ID == '99':
            raise self.exception('Argument \'<using_destination\'> cannot be \'default\' if running on the server (settings.DEVICE=99).')
        if self.is_valid_using(using_destination, 'destination'):
            self._using_destination = using_destination

    def get_using_destination(self):
        if not self._using_destination:
            self.set_using_destination()
        return self._using_destination

    def is_valid_using(self, using, label):
        if not [dbkey for dbkey in settings.DATABASES.iteritems() if dbkey[0] == using]:
            raise ImproperlyConfigured('Expected settings attribute DATABASES to have a NAME key to the \'{1}\'. Got \'{0}\'.'.format(using, label))
        return True
