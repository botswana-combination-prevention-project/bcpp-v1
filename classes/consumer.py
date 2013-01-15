import logging
import sys
from django.conf import settings
from import_history import ImportHistory
from bhp_sync.models import OutgoingTransaction, IncomingTransaction, Producer
from bhp_sync.classes import DeserializeFromTransaction


logger = logging.getLogger(__name__)


class NullHandler(logging.Handler):
    def emit(self, record):
        pass
nullhandler = logger.addHandler(NullHandler())


class Consumer(object):

    def fetch_from_producer(self, producer_hostname):
        db = 'default'
        lock_name = producer_hostname
        producer = self.get_producer(producer_hostname)
        import_history = ImportHistory(db, lock_name)
        if import_history.start():
            n = 0
            tot = OutgoingTransaction.objects.using(producer.settings_key).filter(is_consumed=False).count()
            for outgoing_transaction in OutgoingTransaction.objects.using(producer.settings_key).filter(is_consumed=False):
                if not import_history.locked:
                    break
                n += 1
                if not IncomingTransaction.objects.filter(pk=outgoing_transaction.pk).exists():
                    IncomingTransaction.objects.create(
                        pk=outgoing_transaction.pk,
                        tx_name=outgoing_transaction.tx_name,
                        tx_pk=outgoing_transaction.tx_pk,
                        tx=outgoing_transaction.tx,
                        timestamp=outgoing_transaction.timestamp,
                        producer=outgoing_transaction.producer,
                        action=outgoing_transaction.action)
                    logger.info('{0} / {1} Creating incoming: {2} {3}'. format(n, tot,
                                                                               outgoing_transaction.tx_name,
                                                                               outgoing_transaction.timestamp))
                else:
                    incoming_transaction = IncomingTransaction.objects.get(pk=outgoing_transaction.pk)
                    incoming_transaction.is_consumed = False
                    incoming_transaction.is_error = False
                    incoming_transaction.save()
                    logger.info('{0} / {1} Skipping incoming: {2} {3}. Already exists for pk={4}.'. format(n, tot,
                                                                                                           outgoing_transaction.tx_name,
                                                                                                           outgoing_transaction.timestamp,
                                                                                                           outgoing_transaction.pk))

                outgoing_transaction.is_consumed = True
                outgoing_transaction.save(using=producer.settings_key)
        return import_history.finish()

    def get_producer(self, producer_hostname):
        """Confirm address of producer listed in model matches that listed in settings."""
        if not Producer.objects.filter(settings_key=producer_hostname):
            raise AttributeError('Unknown producer {0}. Not found in producer table.'.format(producer_hostname))
        producer = Producer.objects.get(settings_key=producer_hostname)
        if not producer.settings_key in settings.DATABASES.keys():
            raise AttributeError('Cannot find key in settings.DATABASES for producer {0}. '
                                 'Please add and try again.'.format(producer_hostname))
        if not producer.url.replace('/', '').replace('http:', '') == settings.DATABASES[producer_hostname]['HOST']:
            raise AttributeError('IP address in settings.DATABASES ({0}) does not match that listed '
                                 'in the producer table ({1}) for producer {2}. '
                                 'Please correct.'.format(settings.DATABASES[producer_hostname]['HOST'],
                                                          producer.url.replace('/', '').replace('http:', ''),
                                                          producer_hostname))
        return producer

    def consume(self, lock_name):
        deserialize_from_transaction = DeserializeFromTransaction()
        n = 0
        tot = IncomingTransaction.objects.filter(is_consumed=False).count()
        for incoming_transaction in IncomingTransaction.objects.filter(is_consumed=False).order_by('producer', 'timestamp'):
            n += 1
            action = ''
            print '{0} / {1} {2} {3}'.format(n, tot, incoming_transaction.producer, incoming_transaction.tx_name)
            print '    {0}'.format(incoming_transaction.tx_pk)
            try:
                deserialize_from_transaction.deserialize(incoming_transaction)
                action = 'saved'
            except:
                print "    Unexpected error on consume:", sys.exc_info()[0]
                action = 'exception'
                raise
            print '    {0}'.format(action)

    def copy_incoming_from_server(self):
        if not 'server' in settings.DATABASES.keys():
            raise AttributeError('Cannot find key "server" in settings.DATABASES. '
                                 'Please add and try again.')
        n = 0
        tot = IncomingTransaction.objects.using('server').filter(is_consumed=False).count()
        for incoming_transaction in IncomingTransaction.objects.using('server').filter(is_consumed=False).order_by('producer', 'timestamp'):
            incoming_transaction.save(using='default')
            n += 1
            logger.info('{0} / {1} {2} {3}'.format(n, tot, incoming_transaction.producer, incoming_transaction.tx_name))
