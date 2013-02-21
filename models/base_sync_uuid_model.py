import logging
from datetime import datetime
from django.conf import settings
from django.core import serializers
from django.core.exceptions import ValidationError, ImproperlyConfigured
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

    def is_dispatch_container_model(self):
        """Flags a model as a container model that if dispatched will not appear in DispatchItems, but rather in DispatchContainer."""
        return False

    def ignore_for_dispatch(self):
        """Flgas a model to be ignored by the dispatch infrastructure.

        ..note:: only use this for models that exist in an app listed in the settings.DISPATCH_APP_LABELS but need to be ignored (which should not be very often)."""
        return False

    def include_for_dispatch(self):
        """Flgas a model to be included by the dispatch infrastructure.

        ..note:: only use this for models that do not exist in an app listed in the settings.DISPATCH_APP_LABELS but need to be included (which should not be very often)."""
        return False

    def is_dispatchable_model(self):
        if self.ignore_for_dispatch():
            return False
        if not self._meta.app_label in settings.DISPATCH_APP_LABELS:
            if self.include_for_dispatch():
                return True
            else:
                return False
        return True

#    def get_registered_subject(self):
#        """Primarily needed by bhp_dispatch to return the registered_subject instance.
#
#        Users must override either this or the container method."""
#        if not is_dispatchable_model():
#            return None
#        raise ImproperlyConfigured('Model method get_registered_subject() not configured. Are you attempting to dispatch? Items included for dispatch must have access to registered_subject through this method.')

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
        """Returns True if the model is tracked/is_dispatched=True in the DispatchItem model.

        ..note:: Unlike, :func:`_is_dispatched_to_producer_as_container`, this method does NOT consider
            DispacthContainer. So if the instance is referred to in DispacthContainer but
            not yet tracked in the DispatchItem model, the return value is False."""
        if self.id:
            if self.is_dispatchable_model():
                if self.is_dispatched_to_producer():
                    return True
        return False

#    def unlocking_prep(self):
#        """Override in subclass to run the specific checks for each subclass before unlocking its instance on the server."""
#        pass

    def dispatched_as_container_identifier_attr(self):
        """Override to return the field attrname of the identifier used for the dispatch container."""
        raise ImproperlyConfigured('Method must be overridden on model {0}'.format(self._meta.object_name))

    def _is_dispatched_to_producer_as_container(self):
        is_dispatched = False
        DispatchContainer = get_model('bhp_dispatch', 'DispatchContainer')
        if DispatchContainer:
            is_dispatched = DispatchContainer.objects.filter(
                container_identifier=getattr(self, self.dispatched_as_container_identifier_attr()),
                is_dispatched=True,
                return_datetime__isnull=True).exists()
        return is_dispatched

    def is_dispatched_to_producer(self):
        """Returns lock status as a boolean needed when using this model with bhp_dispatch."""
        is_dispatched = False
        if self.id:
            DispatchItem = get_model('bhp_dispatch', 'DispatchItem')
            if DispatchItem:
                is_dispatched = DispatchItem.objects.filter(
                    item_app_label=self._meta.app_label,
                    item_model_name=self._meta.object_name,
                    item_pk=self.pk,
                    is_dispatched=True).exists()
        return is_dispatched

    def save(self, *args, **kwargs):
        if 'transaction_producer' in kwargs:
            #transaction_producer = kwargs.get('transaction_producer')
            del kwargs['transaction_producer']
        if 'bhp_dispatch' in settings.INSTALLED_APPS:
            from bhp_dispatch.exceptions import AlreadyDispatched
            if self.id:
                if self.is_dispatchable_model():
                    if self.is_dispatch_container_model():
                        if self._is_dispatched_to_producer_as_container():
                            raise AlreadyDispatched('Model {0}-{1} is currently dispatched as a container for other dispatched items.'.format(self._meta.object_name, self.pk))
                    if self.is_dispatched_to_producer():
                        raise AlreadyDispatched('Model {0}-{1} is currently dispatched'.format(self._meta.object_name, self.pk))

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
