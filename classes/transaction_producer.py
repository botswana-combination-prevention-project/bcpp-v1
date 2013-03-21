import socket
import logging
from django.conf import settings
from django.db.models import get_model


logger = logging.getLogger(__name__)


class NullHandler(logging.Handler):
    def emit(self, record):
        pass
nullhandler = logger.addHandler(NullHandler())


class TransactionProducer(object):

    def __init__(self, **kwargs):

        if kwargs.get('hostname'):
            self.value = kwargs.get('hostname')
        else:
            # add on the DB name so that if on the same host still get a unique name
            self.value = '%s-%s' % (socket.gethostname().lower(), settings.DATABASES['default']['NAME'].lower())

    def __get__(self, instance, owner):
        return self.value

    def __str__(self):
        return self.value

    def has_outgoing_transactions(self, using, **kwargs):
        retval = False
        #using = kwargs.get('using', 'default')
        producer_name = kwargs.get('producer_name', self.value)
        OutgoingTransaction = get_model('bhp_sync', 'outgoingtransaction')
        Producer = get_model('bhp_sync', 'producer')
        if OutgoingTransaction.objects.using(using).all().exists():
            if not Producer.objects.using(using).filter(name=producer_name).exists():
                logger.warning('Unknown Producer {0}. Not checking for outgoing transactions. (Note: using database key \'{1}\')'.format(producer_name, using))
            if OutgoingTransaction.objects.using(using).filter(producer=producer_name, is_consumed=False).exists():
                retval = True
        return retval
