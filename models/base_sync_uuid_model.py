import logging
from datetime import datetime
from django.conf import settings
from django.core import serializers
from django.db.models import get_model
from bhp_sync.classes import TransactionProducer
from bhp_base_model.classes import BaseUuidModel


logger = logging.getLogger(__name__)


class NullHandler(logging.Handler):
    def emit(self, record):
        pass
nullhandler = logger.addHandler(NullHandler())


class BaseSyncUuidModel(BaseUuidModel):

    """ Base model for all UUID models and adds synchronization methods and signals. """

    def is_serialized(self, serialize=True):
        if 'ALLOW_MODEL_SERIALIZATION' in dir(settings):
            if settings.ALLOW_MODEL_SERIALIZATION:
                return serialize
        return False

    def deserialize_prep(self):
        """Users may override to manipulate the incoming object before calling save()"""

    def deserialize_on_duplicate(self):
        """Users may override this to determine how to handle a duplicate error on deserialization.

        If you have a way to help decide if a duplicate should overwrite the existing record or not,
        evaluate your criteria here and return True or False. If False is returned to the deserializer,
        the object will not be saved and the transaction WILL be flagged as consumed WITHOUT error.
        """
        logger.info('method deserialize_on_duplicate is not defined, returning True')
        return True

    def deserialize_get_missing_fk(self, attrname):
        """Override to return a foreignkey object for 'attrname', if possible, using criteria in self, otherwise return None"""
        logger.info('method deserialize_get_missing_fk is not defined, raising TypeError()')
        raise TypeError()

    def save(self, *args, **kwargs):
        # sneek in the transaction_producer, if called from
        # view in bhp_sync.
        # get value and delete from kwargs before calling super
        #transaction_producer = TransactionProducer()
        if 'transaction_producer' in kwargs:
            #transaction_producer = kwargs.get('transaction_producer')
            del kwargs['transaction_producer']
        # used 'suppress_autocreate_on_deserialize' to not allow save methods
        # to create new model instances such as appointments, ScheduledEntry, etc
        # as these will be serialized on the producer
        if 'suppress_autocreate_on_deserialize' in kwargs:
            del kwargs['suppress_autocreate_on_deserialize']
        super(BaseSyncUuidModel, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        #TODO: get this to work in pre_delete signal
        transaction_producer = TransactionProducer()
        if 'transaction_producer' in kwargs:
            transaction_producer = kwargs.get('transaction_producer')
            del kwargs['transaction_producer']

        if self.is_serialized() and not self._meta.proxy:

            outgoing_transaction = get_model('bhp_sync', 'outgoingtransaction')
            json_obj = serializers.serialize(
                "json", self.__class__.objects.filter(pk=self.pk), use_natural_keys=True)
            outgoing_transaction.objects.create(
                tx_name=self._meta.object_name,
                tx_pk=self.pk,
                tx=json_obj,
                timestamp=datetime.today().strftime('%Y%m%d%H%M%S%f'),
                producer=str(transaction_producer),
                action='D')
        super(BaseSyncUuidModel, self).delete(*args, **kwargs)

    class Meta:
        abstract = True
