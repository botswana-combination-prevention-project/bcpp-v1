from django.db.models import get_model
from django.core.exceptions import ImproperlyConfigured
from django.conf import settings
from bhp_using.classes import BaseUsing
from bhp_sync.exceptions import ProducerError
from bhp_sync.exceptions import PendingTransactionError


class BaseProducer(BaseUsing):

    def __init__(self, using_source, using_destination, **kwargs):
        super(BaseProducer, self).__init__(using_source, using_destination, **kwargs)
        self._producer = None

    def set_producer(self):
        """Sets the instance of the current producer based on the ORM `using` parameter for the destination.

        .. note:: The producer must always exist on the source."""
        Producer = get_model('bhp_sync', 'Producer')
        if self._producer:
            raise ProducerError('Producer may not be changed once set. Create a new DispatchController instead.')
#        # try to determine producer from using_destination
#        if self.get_using_destination() == 'default':
#            # try to find the producer on the server with hostname + database name
#            settings_key = '{0}-{1}'.format(socket.gethostname().lower(), settings.DATABASES.get('default').get('NAME'))
#            if Producer.objects.using(self.get_using_source()).filter(settings_key=settings_key, is_active=True).exists():
#                self._producer = Producer.objects.using(self.get_using_source()).get(settings_key=settings_key, is_active=True)
#        else:
        if Producer.objects.using(self.get_using_source()).filter(settings_key=self.get_using_destination(), is_active=True).exists():
            self._producer = Producer.objects.using(self.get_using_source()).get(settings_key=self.get_using_destination(), is_active=True)
        if not self._producer:
            raise ProducerError('Dispatcher cannot find a producer with settings key \'{0}\' '
                                                  'on the source {1}.'.format(self.get_using_destination(), self.get_using_source()))
        # check the producers DATABASES key exists
        # TODO: what if producer is "me", e.g settings key is 'default'
        if not self.get_using_destination() == 'default':
            settings_key = self._producer.settings_key
            if not [dbkey for dbkey in settings.DATABASES.iteritems() if dbkey[0] == settings_key]:
                raise ImproperlyConfigured('Dispatcher expects settings attribute DATABASES to have a NAME '
                                           'key to the \'producer\'. Got name=\'{0}\', settings_key=\'{1}\'.'.format(self._producer.name, self._producer.settings_key))

#         # check for pending transactions
#         if self.has_outgoing_transactions():
#             raise PendingTransactionError('Producer \'{0}\' has pending outgoing transactions. Run bhp_sync first.'.format(self.get_producer_name()))

    def get_producer(self):
        """Returns an instance of the current producer."""
        if not self._producer:
            self.set_producer()
        return self._producer

    def get_producer_name(self):
        return self.get_producer().name
