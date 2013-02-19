import logging
from datetime import datetime
from django.conf import settings
from django.core import serializers
from django.core.exceptions import ValidationError
from django.db.models import get_model
from bhp_sync.classes import TransactionProducer
from bhp_base_model.models import BaseUuidModel


logger = logging.getLogger(__name__)


class NullHandler(logging.Handler):
    def emit(self, record):
        pass
nullhandler = logger.addHandler(NullHandler())


class BaseSyncUuidModel(BaseUuidModel):

    """Base model for all UUID models and adds synchronization methods and signals. """

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

    @property
    def is_dispatched(self):
        """Returns lock status as a boolean needed when using this model with bhp_dispatch."""
        is_dispatched, producer = self.is_dispatched_to_producer()
        return is_dispatched

    def is_dispatched_to_producer(self, subject_identifier=None):
        """Returns lock status as a boolean needed when using this model with bhp_dispatch."""
        is_dispatched = False
        producer = None
        if not subject_identifier:
            if 'get_subject_identifier' in dir(self):
                self.get_subject_identifier()
        DispatchItem = get_model('bhp_dispatch', 'DispatchItem')
        if DispatchItem and subject_identifier:
            if DispatchItem.objects.filter(
                    subject_identifiers__icontains=subject_identifier,
                    is_dispatched=True).exists():
                dispatch_item = DispatchItem.objects.get(
                    subject_identifiers__icontains=subject_identifier,
                    is_dispatched=True)
                producer = dispatch_item.producer
                is_dispatched = True
        return (is_dispatched, producer)

    def save(self, *args, **kwargs):
        if 'transaction_producer' in kwargs:
            #transaction_producer = kwargs.get('transaction_producer')
            del kwargs['transaction_producer']
        # for bhp_dispatch, catch instances that may not be saved
        if 'bhp_dispatch' in settings.INSTALLED_APPS:
            is_dispatched, producer = self.is_dispatched_to_producer()
            if is_dispatched:
                raise ValidationError('Save not allowed. Model {0} for subject {1} is currently dispatched to {3}.'
                                  '(You should catch this in the form validation.)'.format(self._meta.object_name,
                                                                                           self.get_subject_identifier(),
                                                                                           producer))
        super(BaseSyncUuidModel, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        """Deletes"""
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
