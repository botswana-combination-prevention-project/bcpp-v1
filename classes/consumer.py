import logging
import sys
from django.db.models import get_model
from bhp_sync.classes import DeserializeFromTransaction
from bhp_sync.exceptions import TransactionConsumerError
from base import Base


logger = logging.getLogger(__name__)


class NullHandler(logging.Handler):
    def emit(self, record):
        pass
nullhandler = logger.addHandler(NullHandler())


class Consumer(Base):

    def consume(self, lock_name=None, **kwargs):
        """Consumes ALL incoming transactions on \'using\' in order by ('producer', 'timestamp')."""
        IncomingTransaction = get_model('bhp_sync', 'IncomingTransaction')
        check_hostname = kwargs.get('check_hostname', True)
        deserialize_from_transaction = DeserializeFromTransaction(using=self.get_using())
        tot = IncomingTransaction.objects.using(self.get_using()).filter(is_consumed=False).count()
        for n, incoming_transaction in enumerate(IncomingTransaction.objects.using(self.get_using()).filter(is_consumed=False, is_ignored=False).order_by('producer', 'timestamp')):
            action = ''
            print '{0} / {1} {2} {3}'.format(n + 1, tot, incoming_transaction.producer, incoming_transaction.tx_name)
            print '    {0}'.format(incoming_transaction.tx_pk)
            try:
                deserialize_from_transaction.deserialize(incoming_transaction, check_hostname=check_hostname)
                action = 'saved'
            except:
                print "    Unexpected error on consume:", sys.exc_info()[0]
                action = 'exception'
                raise TransactionConsumerError('Unexpected error when consuming incoming transactions.')
            print '    {0}'.format(action)

    def fetch_outgoing(self, source):
        """Fetches all OutgoingTransactions not consumed from a source."""
        if source == self.get_using():
            raise TransactionConsumerError('Cannot fetch outgoing transactions from myself')
        if self.verify_using(source):
            OutgoingTransaction = get_model('bhp_sync', 'OutgoingTransaction')
            IncomingTransaction = get_model('bhp_sync', 'IncomingTransaction')
            for outgoing_transaction in OutgoingTransaction.objects.using(source).filter(is_consumed=False):
                new_incoming_transaction = IncomingTransaction()
                for field in OutgoingTransaction._meta.fields:
                    if field.attname not in ['id', 'is_consumed']:
                        setattr(new_incoming_transaction, field.attname, getattr(outgoing_transaction, field.attname))
                new_incoming_transaction.is_consumed = False
                new_incoming_transaction.save(using=self.get_using())
                outgoing_transaction.is_consumed = True
                outgoing_transaction.save(using=source)

#    def check_all_synched_from_producer(self, producer_name):
#        OutgoingTransaction = get_model('bhp_sync', 'OutgoingTransaction')
#        producer = self.get_producer(producer_name)
#        using = producer.settings_key
#        tot = OutgoingTransaction.objects.using(using).filter(is_consumed=False, producer=producer_name).count()
#        if tot > 0:
#            raise PendingTransactionError('Outgoing transactions exist on producer {0}. Please sync the producer and try again.'.format(producer_name))
#
#    def check_all_consumed_in_server(self, producer_name):
#        IncomingTransaction = get_model('bhp_sync', 'IncomingTransaction')
#        tot = IncomingTransaction.objects.using(self.get_using_server()).filter(is_consumed=False, producer=producer_name).count()
#        if tot > 0:
#            raise PendingTransactionError('Incoming transactions exist on the server for producer {0}. Please consume transactions and try again.'.format(producer_name))
#
#    def fetch_from_producer(self, producer_name):
#        OutgoingTransaction = get_model('bhp_sync', 'OutgoingTransaction')
#        IncomingTransaction = get_model('bhp_sync', 'IncomingTransaction')
#        db = self.get_using()
#        lock_name = producer_name
#        producer = self.get_producer(producer_name)
#        import_history = ImportHistory(db, lock_name)
#        if import_history.start():
#            n = 0
#            tot = OutgoingTransaction.objects.using(producer.settings_key).filter(is_consumed=False).count()
#            for outgoing_transaction in OutgoingTransaction.objects.using(producer.settings_key).filter(is_consumed=False):
#                if not import_history.locked:
#                    break
#                n += 1
#                if not IncomingTransaction.objects.filter(pk=outgoing_transaction.pk).exists():
#                    IncomingTransaction.objects.create(
#                        pk=outgoing_transaction.pk,
#                        tx_name=outgoing_transaction.tx_name,
#                        tx_pk=outgoing_transaction.tx_pk,
#                        tx=outgoing_transaction.tx,
#                        timestamp=outgoing_transaction.timestamp,
#                        producer=outgoing_transaction.producer,
#                        action=outgoing_transaction.action)
#                    logger.info('{0} / {1} Creating incoming: {2} {3}'. format(n, tot,
#                                                                               outgoing_transaction.tx_name,
#                                                                               outgoing_transaction.timestamp))
#                else:
#                    incoming_transaction = IncomingTransaction.objects.get(pk=outgoing_transaction.pk)
#                    incoming_transaction.is_consumed = False
#                    incoming_transaction.is_error = False
#                    incoming_transaction.save()
#                    logger.info('{0} / {1} Skipping incoming: {2} {3}. Already exists for pk={4}.'. format(n, tot,
#                                                                                                           outgoing_transaction.tx_name,
#                                                                                                           outgoing_transaction.timestamp,
#                                                                                                           outgoing_transaction.pk))
#
#                outgoing_transaction.is_consumed = True
#                outgoing_transaction.save(using=producer.settings_key)
#        return import_history.finish()
#
#    def get_producer(self, producer_name):
#        """Confirm address of producer listed in model matches that listed in settings."""
#        Producer = get_model('bhp_sync', 'Producer')
#        if not Producer.objects.filter(settings_key=producer_name):
#            raise AttributeError('Unknown producer {0}. Not found in producer table.'.format(producer_name))
#        producer = Producer.objects.get(settings_key=producer_name)
#        if not producer.settings_key in settings.DATABASES.keys():
#            raise AttributeError('Cannot find key in settings.DATABASES for producer {0}. '
#                                 'Please add and try again.'.format(producer_name))
#        if not producer.url.replace('/', '').replace('http:', '') == settings.DATABASES[producer_name]['HOST']:
#            raise AttributeError('IP address in settings.DATABASES ({0}) does not match that listed '
#                                 'in the producer table ({1}) for producer {2}. '
#                                 'Please correct.'.format(settings.DATABASES[producer_name]['HOST'],
#                                                          producer.url.replace('/', '').replace('http:', ''),
#                                                          producer_name))
#        return producer


